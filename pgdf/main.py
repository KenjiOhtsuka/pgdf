import argparse
import re
import xlsxwriter
from enum import Enum

from pgdf.blame import FileBlame, LineBlame
from pgdf.git import get_label, get_summary, get_diff, get_blame, get_log


class OutputFormat(Enum):
    EXCEL = 'excel'
    CSV = 'csv'
    TSV = 'tsv'


class Column:
    def __init__(self, index: int, width: int = None):
        """

        :param index: column position that starts from 0.
        :param width:
        """
        self.index = index
        self.width = width

    def __str__(self):
        return f'{self.index}(width={self.width})'

    def __repr__(self):
        return self.__str__()


def main() -> None:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="""
This is a tool to convert markdown file to excel.
""",
        epilog="""
== Example Use Case ==

# Initialize the directory
% pgdf init .

# Create some markdown files in the directory 

# Build the Excel file
% pgdf build .
"""
    )
    parser.add_argument('revision_1', help='The first branch, tag name or revision to be compared')
    parser.add_argument('revision_2', help='The first branch, tag name or revision be compared')
    parser.add_argument("path", help="The file path to be compared", nargs='*')

    args = parser.parse_args()

    revision_1 = args.revision_1
    revision_2 = args.revision_2
    paths = args.path

    label = get_label()

    output_file_path = f'diff_{revision_1}..{revision_2}.xlsx'.replace('/', '_')
    workbook = xlsxwriter.Workbook(output_file_path)

    commit_hash_column = Column(0, 10)
    commit_author_column = Column(commit_hash_column.index + 1, 10)
    commit_datetime_column = Column(commit_author_column.index + 1, 15)
    commit_comment_column = Column(commit_datetime_column.index + 1, 20)
    before_line_num_column = Column(commit_comment_column.index + 1, 5)
    after_line_num_column = Column(before_line_num_column.index + 1, 5)
    code_column = Column(after_line_num_column.index + 1, 100)
    columns = [
        commit_hash_column, commit_author_column, commit_datetime_column, commit_comment_column,
        before_line_num_column, after_line_num_column, code_column
    ]


    class Format:
        @staticmethod
        def build_format(kwargs):
            basic_format_properties = {'font_name': 'Consolas'}
            return workbook.add_format(dict(basic_format_properties, **kwargs))

        BASIC = build_format({})
        """Basic format. Just Consolas font."""
        WRAP_BASIC = build_format({'text_wrap': True})
        """Basic format with text wrap."""
        BOLD = build_format({'bold': True})
        """Basic format with bold."""
        WRAP_BOLD = build_format({'text_wrap': True, 'bold': True})
        """Basic format with text wrap and bold."""
        RED = build_format({'font_color': 'red', 'bg_color': '#FFCCCC'})
        """Basic format with red font and light red background."""
        WRAP_RED = build_format({'text_wrap': True, 'font_color': 'red', 'bg_color': '#FFCCCC'})
        """Basic format with text wrap, red font and light red background."""
        GREEN = build_format({'font_color': 'green', 'bg_color': '#CCFFCC'})
        """Basic format with green font and light green background."""
        WRAP_GREEN = build_format({'text_wrap': True, 'font_color': 'green', 'bg_color': '#CCFFCC'})
        """Basic format with text wrap, green font and light green background."""
        FORE_BLUE = build_format({'font_color': 'blue'})
        """Basic format with blue font."""
        WRAP_FORE_BLUE = build_format({'text_wrap': True, 'font_color': 'blue'})
        """Basic format with text wrap and blue font."""
        FORE_GREEN = build_format({'font_color': 'green'})
        """Basic format with green font."""
        WRAP_FORE_GREEN = build_format({'text_wrap': True, 'font_color': 'green'})
        """Basic format with text wrap and green font."""
        FORE_GREEN_BOLD = build_format({'font_color': 'green', 'bold': True})
        """Basic format with green font and bold."""
        WRAP_FORE_GREEN_BOLD = build_format({'text_wrap': True, 'font_color': 'green', 'bold': True})
        """Basic format with text wrap, green font and bold."""
        FORE_RED = build_format({'font_color': 'red'})
        """Basic format with red font."""
        WRAP_FORE_RED = build_format({'text_wrap': True, 'font_color': 'red'})
        """Basic format with text wrap and red font."""
        FORE_RED_BOLD = build_format({'font_color': 'red', 'bold': True})
        """Basic format with red font and bold."""
        WRAP_FORE_RED_BOLD = build_format({'text_wrap': True, 'font_color': 'red', 'bold': True})
        """Basic format with text wrap, red font and bold."""

    # Write Summary
    worksheet = workbook.add_worksheet("Summary")
    worksheet.set_column(0, 0, 60)

    result_text = get_summary(revision_1, revision_2, paths)

    worksheet.write_string(0, 0, (f'Diff {revision_1} {revision_2} ' + ' '.join(paths)).strip(), Format.BASIC)
    row_index = 2

    for line in result_text.splitlines():
        rm = re.match(r'^\s(?P<path>.*?)\s+\|\s+(?P<change>\d+)\s+(?P<note>[-+]*)\s*$', line)
        if rm:
            path = rm.group('path')
            change = rm.group('change')
            note = rm.group('note')
            plus = note.count('+') if note is not None else 0
            minus = note.count('-') if note is not None else 0

            worksheet.write_string(row_index, 0, path, Format.BASIC)
            worksheet.write_number(row_index, 1, int(change), Format.BASIC)
            args = []
            if plus > 0:
                args.append(Format.FORE_GREEN)
                args.append('+' * plus)
            if minus > 0:
                args.append(Format.FORE_RED)
                args.append('-' * minus)

            if len(args) > 2:
                worksheet.write_rich_string(row_index, 2, *args)
            else:
                worksheet.write_string(row_index, 2, args[1], args[0])
            row_index += 1
            continue

        rm = re.match(r'^\s(?P<path>.*?)\s+\|\s+Bin\s+(?P<before>\d+) -> (?P<after>\d+) bytes\s*$', line)
        if rm:
            worksheet.write_string(row_index, 0, path, Format.BASIC)
            worksheet.write_string(row_index, 1, 'Bin', Format.BASIC)
            worksheet.write_rich_string(
                row_index, 2,
                Format.FORE_RED, rm.group("before"),
                Format.BASIC, ' -> ',
                Format.GREEN, rm.group("after"),
                Format.BASIC, ' bytes'
            )
            row_index += 1
            continue

        worksheet.write_string(row_index, 0, line, Format.BASIC)
        row_index += 1

    # Write Diff
    worksheet = workbook.add_worksheet("Diff")
    for column in columns:
        worksheet.set_column(column.index, column.index, column.width)

    result_text = get_diff(revision_1, revision_2, paths)

    before_line_number = 0
    after_line_number = 0

    worksheet.write_string(0, 0, (f'Diff {revision_1} {revision_2} ' + ' '.join(paths)).strip(), Format.BASIC)

    row_index = 1
    revisions = set()
    logs = {}

    for line in result_text.splitlines():
        if line.startswith('diff'):
            row_index += 1
            worksheet.write_string(row_index, code_column.index, line, Format.BOLD)
            blame = {
                'before': None,
                'after': None
            }
        elif line.startswith('---'):
            rm = re.match(r'^--- a/(?P<file_path>.*)$', line)
            if rm:
                path = rm.group('file_path').strip()
                blame['before'] = FileBlame(path)
            worksheet.write_string(row_index, code_column.index, line, Format.FORE_RED_BOLD)
        elif line.startswith('+++'):
            rm = re.match(r'^\+\+\+ b/(?P<file_path>.*)$', line)
            if rm:
                path = rm.group('file_path').strip()
                blame['after'] = FileBlame(path)
            worksheet.write_string(row_index, code_column.index, line, Format.FORE_GREEN_BOLD)
        elif line.startswith('+'):
            line_blame = revision_2_blame[after_line_number]
            worksheet.write_string(row_index, commit_hash_column.index, line_blame.commit_hash, Format.GREEN)
            worksheet.write_string(row_index, commit_author_column.index, line_blame.author, Format.GREEN)
            worksheet.write_string(row_index, commit_datetime_column.index, line_blame.datetime, Format.GREEN)
            worksheet.write_string(row_index, commit_comment_column.index, logs[line_blame.commit_hash], Format.GREEN)
            worksheet.write_string(row_index, before_line_num_column.index, '', Format.GREEN)
            worksheet.write_number(row_index, after_line_num_column.index, after_line_number, Format.GREEN)
            worksheet.write_string(row_index, code_column.index, line, Format.WRAP_GREEN)
            after_line_number += 1
        elif line.startswith('-'):
            line_blame = revision_1_blame[before_line_number]
            worksheet.write_string(row_index, commit_hash_column.index, line_blame.commit_hash, Format.RED)
            worksheet.write_string(row_index, commit_author_column.index, line_blame.author, Format.RED)
            worksheet.write_string(row_index, commit_datetime_column.index, line_blame.datetime, Format.RED)
            worksheet.write_string(row_index, commit_comment_column.index, logs[line_blame.commit_hash], Format.RED)
            worksheet.write_number(row_index, before_line_num_column.index, before_line_number, Format.RED)
            worksheet.write_string(row_index, after_line_num_column.index, '', Format.RED)
            worksheet.write_string(row_index, code_column.index, line, Format.WRAP_RED)
            before_line_number += 1
        elif line.startswith('@@'):
            row_index += 1
            sr = re.search(r'^(?P<navigation>@@ .* @@)(?P<part_name>.*)$', line)
            navigation = sr.group('navigation')
            part_name = sr.group('part_name')

            sr = re.search(r'^@@ -(?P<before_range>(?P<before_line_number>\d+),?(?P<before_line_volume>\d+)?) \+(?P<after_range>(?P<after_line_number>\d+),?(?P<after_line_volume>\d+)?) @@$', navigation)

            before_line_number = int(sr.group('before_line_number'))
            before_line_volume = sr.group('before_line_volume')
            before_line_volume = before_line_number if before_line_volume is None or before_line_volume == '' else int(before_line_volume)
            after_line_number = int(sr.group('after_line_number'))
            after_line_volume = sr.group('after_line_volume')
            after_line_volume = after_line_number if after_line_volume is None or after_line_volume == '' else int(after_line_volume)
            if part_name is None or part_name.isspace() or part_name == '':
                worksheet.write_string(row_index, code_column.index, str(navigation), Format.FORE_BLUE)
            else:
                worksheet.write_rich_string(row_index, code_column.index, Format.FORE_BLUE, str(navigation), Format.BASIC, str(part_name))

            # get the file blame
            if blame['before']:
                result_text = get_blame(revision_1, blame['before'].path, before_line_number, before_line_volume)
                revision_1_blame = {
                    b.line_number: b for b in [LineBlame.parse(line) for line in result_text.splitlines()]
                }
            else:
                revision_1_blame = {}

            if blame['after']:
                result_text = get_blame(revision_2, blame['after'].path, after_line_number, after_line_volume)
                revision_2_blame = {
                    b.line_number: b for b in [LineBlame.parse(line) for line in result_text.splitlines()]
                }
            else:
                revision_2_blame = {}

            current_revisions = set(b.commit_hash for b in revision_2_blame.values()).union(
                set(b.commit_hash for b in revision_1_blame.values())
            )
            new_revisions = current_revisions - revisions

            for revision in new_revisions:
                logs[revision] = re.sub(r'^"(.*)"$', r'\1', get_log(revision).strip())

            revisions = revisions.union(new_revisions)

        elif line.startswith(' '):
            worksheet.write_number(row_index, after_line_num_column.index, after_line_number, Format.BASIC)
            worksheet.write_number(row_index, before_line_num_column.index, before_line_number, Format.BASIC)
            worksheet.write_string(row_index, code_column.index, line, Format.WRAP_BASIC)
            before_line_number += 1
            after_line_number += 1
        else:
            worksheet.write_string(row_index, code_column.index, line, Format.WRAP_BASIC)

        row_index += 1

    workbook.close()

    print(f'{output_file_path} was generated.')


if __name__ == '__main__':
    main()

