import re


class FileSummary:
    def __init__(self, file_path, change_count, add_count, delete_count):
        self.file_path = file_path
        self.change_count = change_count
        self.add_count = add_count
        self.delete_count = delete_count
        print(add_count, delete_count)

    @staticmethod
    def parse(line):
        """
        Parse the line and return FileSummary object.

        >>> fs = FileSummary.parse(' src/pgdf/main.py |  2 +-')
        >>> (fs.file_path, fs.change_count, fs.add_count, fs.delete_count)
        ('src/pgdf/main.py', 2, 1, 1)

        >>> fs = FileSummary.parse(' src/pgdf/sub.py |  6 ++++--')
        >>> (fs.file_path, fs.change_count, fs.add_count, fs.delete_count)
        ('src/pgdf/sub.py', 6, 4, 2)

        >>> fs = FileSummary.parse(' src/common/dw_service.ts                                   | 78 +++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------------')
        >>> (fs.file_path, fs.change_count, fs.add_count, fs.delete_count)
        ('src/common/dw_service.ts', 78, 53, 25)

        :param line:
        :return:
        """
        print(line)
        m = re.match(r'^\s*(?P<file_path>.+?)\s+\|\s+(?P<change_count>\d+)\s(?P<change_note>[-+]*)\s*$', line)
        if m:
            file_path = m.group('file_path')
            change_count = int(m.group('change_count'))
            change_note = m.group('change_note')
            add_count = change_note.count('+')
            delete_count = change_note.count('-')
            print(add_count, delete_count, change_note)
            return FileSummary(file_path, change_count, add_count, delete_count)
        return None

    def __str__(self):
        return ' {} | {} {}{}'.format(self.file_path, self.change_count, '+' * self.add_count, '-' * self.delete_count)


class Summary:
    def __init__(self):
        self.file_summaries = []

    def append(self, file_summary: FileSummary):
        self.file_summaries.append(file_summary)

    @staticmethod
    def parse(text):
        """
        Parse the text and return Summary object.

        >>> s = Summary.parse(' 1 file changed, 2 insertions(+), 1 deletion(-)')
        >>> (s.file_summaries[0].file_path, s.file_summaries[0].change_count, s.file_summaries[0].add_count, s.file_summaries[0].delete_count)
        ('1 file changed', 2, 2, 1)

        >>> s = Summary.parse(' 2 files changed, 6 insertions(+), 2 deletions(-)')
        >>> (s.file_summaries[0].file_path, s.file_summaries[0].change_count, s.file_summaries[0].add_count, s.file_summaries[0].delete_count)
        ('2 files changed', 8, 6, 2)

        :param text:
        :return:
        """
        s = Summary()
        lines = text.splitlines()
        line_count = len(lines)
        added_line_count = 0
        for line in lines:
            fs = FileSummary.parse(line)
            if fs:
                s.file_summaries.append(fs)
                added_line_count += 1
        assert line_count == added_line_count + 1, 'Something went wrong - line count: {}, added line count: {}'.format(line_count, added_line_count)
        return s

    def __str__(self):
        result = ''
        max_length_of_file_path = max([len(fs.file_path) for fs in self.file_summaries])
        max_length_of_change = max([len(str(fs.change_count)) for fs in self.file_summaries])
        for fs in self.file_summaries:
            result += f' {{:<{max_length_of_file_path}}} | {{:<{max_length_of_change}}} {{}} {{}}'.format(fs.file_path, str(fs.change_count), '+' * fs.add_count, '-' * fs.delete_count) + '\n'
        return result
