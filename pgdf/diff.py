import re

class FileDiff:
    def __init__(self):
        self.before_file_path = None
        self.after_file_path = None
        self.summary_lines = []
        self.diff_parts = []

    @staticmethod
    def parse(lines):
        """
        Parse the lines and return FileDiff object.

        >>> fd = FileDiff.parse(['diff --git a/.gitignore b/.gitignore', 'new file mode 100644', 'index 0000000..74be068', '--- /dev/null', '+++ b/.gitignore', '@@ -0,0 +1,13 @@', '+# for Intellij IDEA', '+.idea', '+mael.iml', '+', '+# for editable package', '+mael.egg-info', '+__pycache__', '+', '+# compiled packages', '+dist', '+', '+# credentials', '+.pypirc'])
        >>> fd.file_path
        '.gitignore'
        >>> fd.diff_lines
        ['diff --git a/.gitignore b/.gitignore', 'new file mode 100644', 'index 0000000..74be068', '--- /dev/null', '+++ b/.gitignore', '@@ -0,0 +1,13 @@', '+# for Intellij IDEA', '+.idea', '+mael.iml', '+', '+# for editable package', '+mael.egg-info', '+__pycache__', '+', '+# compiled packages', '+dist', '+', '+# credentials', '+.pypirc']

        :param lines:
        :return:
        """
        m = re.match(r'^diff --git a/(?P<file_path>.+?) b/(?P=file_path>.+?)$', lines[0])
        if m:
            file_path = m.group('file_path')
            diff_lines = lines
            return FileDiff(file_path, diff_lines)
        return None


class Diff:
    @staticmethod
    def parse(text):
        lines = text.splitlines()
        file_diffs = []
        file_diff = None
        for line in lines:
            if line.startswith('diff '):
                if file_diff:
                    file_diffs.append(file_diff)
                file_diff = FileDiff.parse([line])
                print(line)
                continue
            if line.startswith('index '):
                print(line)
                continue
            if line.startswith('--- '):
                print(line)
                continue
            if line.startswith('+++ '):
                print(line)
                continue
            if line.startswith('@@ '):
                print(line)
                continue
            if line.startswith('-'):
                print(line)
                continue
            if line.startswith('+'):
                print(line)
                continue
            if line.startswith(' '):
                print(line)
                continue

