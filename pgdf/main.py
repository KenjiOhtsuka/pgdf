import argparse
import re
import xlsxwriter
from enum import Enum

from pgdf.blame import FileBlame, LineBlame
from pgdf.git import get_label, get_summary, get_diff, get_blame


class OutputFormat(Enum):
    EXCEL = 'excel'
    CSV = 'csv'
    TSV = 'tsv'


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

    args = parser.parse_args()

    revision_1 = args.revision_1
    revision_2 = args.revision_2

    # if args.directory:
    #     if os.path.isabs(args.directory):
    #         target_dir = args.directory
    #     else:
    #         target_dir = os.path.join(os.getcwd(), args.directory)
    # else:
    #     target_dir = os.getcwd()
    #
    # if args.command == 'init':
    #     # create init file
    #     i = Initializer(target_dir)
    #     i.initialize()
    # elif args.command == 'build':
    #     # read the directory and save the Excel file
    #     convert(target_dir, args.environment, args.format)
    # elif args.command == 'inspect':
    #     # read the directory and get into REPL
    #     repl(target_dir, args.environment)


    label = get_label()

    commit_number_column = 0
    commit_author_column = commit_number_column + 1
    commit_datetime_column = commit_author_column + 1
    before_line_num_column = commit_datetime_column + 1
    after_line_num_column = before_line_num_column + 1
    code_column = after_line_num_column + 1

    workbook = xlsxwriter.Workbook(f'diff_{revision_1}.{revision_2}.xlsx'.replace('/', '_'))
    # define formats

    class Format:
        @staticmethod
        def build_format(kwargs):
            basic_format_properties = {'font_name': 'Consolas'}
            return workbook.add_format(dict(basic_format_properties, **kwargs))

        BASIC = build_format({})
        WRAP_BASIC = build_format({'text_wrap': True})
        BOLD = build_format({'bold': True})
        WRAP_BOLD = build_format({'text_wrap': True, 'bold': True})
        RED = build_format({'font_color': 'red', 'bg_color': '#FFCCCC'})
        WRAP_RED = build_format({'text_wrap': True, 'font_color': 'red', 'bg_color': '#FFCCCC'})
        GREEN = build_format({'font_color': 'green', 'bg_color': '#CCFFCC'})
        WRAP_GREEN = build_format({'text_wrap': True, 'font_color': 'green', 'bg_color': '#CCFFCC'})
        FORE_BLUE = build_format({'font_color': 'blue'})
        WRAP_FORE_BLUE = build_format({'text_wrap': True, 'font_color': 'blue'})
        FORE_GREEN = build_format({'font_color': 'green'})
        WRAP_FORE_GREEN = build_format({'text_wrap': True, 'font_color': 'green'})
        FORE_GREEN_BOLD = build_format({'font_color': 'green', 'bold': True})
        WRAP_FORE_GREEN_BOLD = build_format({'text_wrap': True, 'font_color': 'green', 'bold': True})
        FORE_RED = build_format({'font_color': 'red'})
        WRAP_FORE_RED = build_format({'text_wrap': True, 'font_color': 'red'})
        FORE_RED_BOLD = build_format({'font_color': 'red', 'bold': True})
        WRAP_FORE_RED_BOLD = build_format({'text_wrap': True, 'font_color': 'red', 'bold': True})

    # Write Summary
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, 0, 60)

    result_text = get_summary(revision_1, revision_2)
    # summary = Summary.parse(result_text)

    worksheet.write_string(0, 0, f'Diff {revision_1} {revision_2}', Format.BASIC)
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

            print(args)
            if len(args) > 2:
                worksheet.write_rich_string(row_index, 2, *args)
            else:
                worksheet.write_string(row_index, 2, args[1], args[0])
        else:
            worksheet.write_string(row_index, 0, line, Format.BASIC)

        row_index += 1

    # Write Diff
    worksheet = workbook.add_worksheet()
    worksheet.set_column(code_column, code_column, 100)

    result_text = get_diff(revision_1, revision_2)

    before_line_number = 0
    after_line_number = 0

    worksheet.write_string(0, 0, f'Diff {revision_1} {revision_2}', Format.BASIC)

    row_index = 1

    for line in result_text.splitlines():
        if line.startswith('diff'):
            row_index += 1
            worksheet.write_string(row_index, code_column, line, Format.BOLD)
            blame = {
                'before': None,
                'after': None
            }
        elif line.startswith('---'):
            rm = re.match(r'^--- a/(?P<file_path>.*)$', line)
            if rm:
                path = rm.group('file_path').strip()
                blame['before'] = FileBlame(path)
            worksheet.write_string(row_index, code_column, line, Format.FORE_RED_BOLD)
        elif line.startswith('+++'):
            rm = re.match(r'^\+\+\+ b/(?P<file_path>.*)$', line)
            if rm:
                path = rm.group('file_path').strip()
                blame['after'] = FileBlame(path)
            worksheet.write_string(row_index, code_column, line, Format.FORE_GREEN_BOLD)
        elif line.startswith('+'):
            line_blame = revision_2_blame[after_line_number]
            worksheet.write_string(row_index, commit_number_column, line_blame.commit_hash, Format.GREEN)
            worksheet.write_string(row_index, commit_author_column, line_blame.author, Format.GREEN)
            worksheet.write_string(row_index, commit_datetime_column, line_blame.datetime, Format.GREEN)
            worksheet.write_string(row_index, before_line_num_column, '', Format.GREEN)
            worksheet.write_number(row_index, after_line_num_column, after_line_number, Format.GREEN)
            worksheet.write_string(row_index, code_column, line, Format.WRAP_GREEN)
            after_line_number += 1
        elif line.startswith('-'):
            line_blame = revision_1_blame[before_line_number]
            worksheet.write_string(row_index, commit_number_column, line_blame.commit_hash, Format.RED)
            worksheet.write_string(row_index, commit_author_column, line_blame.author, Format.RED)
            worksheet.write_string(row_index, commit_datetime_column, line_blame.datetime, Format.RED)
            worksheet.write_number(row_index, before_line_num_column, before_line_number, Format.RED)
            worksheet.write_string(row_index, after_line_num_column, '', Format.RED)
            worksheet.write_string(row_index, code_column, line, Format.WRAP_RED)
            before_line_number += 1
        elif line.startswith('@@'):
            row_index += 1
            sr = re.search(r'^(?P<navigation>@@ .* @@)(?P<part_name>.*)$', line)
            navigation = sr.group('navigation')
            part_name = sr.group('part_name')

            sr = re.search(r'^@@ -(?P<before_range>(?P<before_line_number>\d+),?(?P<before_line_volume>\d+)?) \+(?P<after_range>(?P<after_line_number>\d+),?(?P<after_line_volume>\d+)?) @@$', navigation)
            if sr:
                pass
            #sr = re.search(r'^@@ -(?P<before_line_number>\d+),?(?P<before_line_volume>\d+)? \+(?P<after_line_number>\d+),?(?P<after_line_volume>\d+)? @@$', navigation)
            before_range = sr.group('before_range')
            before_line_number = int(sr.group('before_line_number'))
            before_line_volume = sr.group('before_line_volume')
            before_line_volume = before_line_number if before_line_volume is None or before_line_volume == '' else int(before_line_volume)
            after_range = sr.group('after_range')
            after_line_number = int(sr.group('after_line_number'))
            after_line_volume = sr.group('after_line_volume')
            after_line_volume = after_line_number if after_line_volume is None or after_line_volume == '' else int(after_line_volume)
            if part_name is None or part_name.isspace() or part_name == '':
                worksheet.write_string(row_index, code_column, str(navigation), Format.FORE_BLUE)
            else:
                worksheet.write_rich_string(row_index, code_column, Format.FORE_BLUE, str(navigation), Format.BASIC, str(part_name))

            # get the file blame
            if blame['before']:
                result_text = get_blame(revision_1, blame['before'].path, before_line_number, before_line_volume)
                revision_1_blame = {
                    b.line_number: b for b in [LineBlame.parse(line) for line in result_text.splitlines()]
                }

            if blame['after']:
                result_text = get_blame(revision_2, blame['after'].path, after_line_number, after_line_volume)
                revision_2_blame = {
                    b.line_number: b for b in [LineBlame.parse(line) for line in result_text.splitlines()]
                }


            # to get revision comment
            # git show --format="%s" -s revision_1

        elif line.startswith(' '):
            worksheet.write_number(row_index, after_line_num_column, after_line_number, Format.BASIC)
            worksheet.write_number(row_index, before_line_num_column, before_line_number, Format.BASIC)
            worksheet.write_string(row_index, code_column, line, Format.WRAP_BASIC)
            before_line_number += 1
            after_line_number += 1
        else:
            worksheet.write_string(row_index, code_column, line, Format.WRAP_BASIC)

        row_index += 1

    workbook.close()

    #print(result_text)

    # result = subprocess.run(['git', 'blame', revision_1, '--', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # if result.returncode != 0:
    #     print(result.stderr.decode('utf-8'))
    #     exit(result.returncode)


# os.execlp("git diff --stat", args)

if __name__ == '__main__':
    import traceback
    import warnings
    def warn_with_traceback(message, category, filename, lineno, file=None, line=None):

        log = file if hasattr(file,'write') else sys.stderr
        traceback.print_stack(file=log)
        log.write(warnings.formatwarning(message, category, filename, lineno, line))

    warnings.simplefilter("always")
    warnings.showwarning = warn_with_traceback
    main()

# TODO:
#   * font configuration
