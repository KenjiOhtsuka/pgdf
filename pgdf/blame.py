import re


class FileBlame:
    def __init__(self, path):
        self.path = path
        self.lines = {}


class LineBlame:
    def __init__(self, commit_hash, author, datetime, line_number, line):
        self.commit_hash = commit_hash
        self.author = author
        self.datetime = datetime
        self.line_number = line_number
        self.line = line

    @staticmethod
    def parse(line) -> 'LineBlame':
        """
        Parse a line blame from a line.

        >>> blame = LineBlame.parse('0e2b5b3c (Kenji Otsuka 2019-11-04 23:04:00 +0900  1) import re')
        >>> blame.commit_hash
        '0e2b5b3c'
        >>> blame.author
        'Kenji Otsuka'
        >>> blame.datetime
        '2019-11-04 23:04:00 +0900'
        >>> blame.line_number
        1

        >>> blame = LineBlame.parse('8e30324f6 (kenjiotsuka   2022-01-07 15:04:40 +0900 1085) // アクセストークン取得')
        >>> blame.commit_hash
        '8e30324f6'
        >>> blame.author
        'kenjiotsuka'
        >>> blame.datetime
        '2022-01-07 15:04:40 +0900'
        >>> blame.line_number
        1085

        :param line: like '0e2b5b3c (Kenji Otsuka 2019-11-04 23:04:00 +0900  1) import re'
        :return:
        """
        # print(line)
        m = re.match(r'^\s*(?P<commit_hash>[\^0-9a-f]{6,40})\s+(.+\s+){0,1}\((?P<author>.+)\s+(?P<datetime>(?P<date>[-\d]+?) (?P<time>[:\d]*?) (?P<timezone>.*?))\s+(?P<line_number>\d+)\)\s+(?P<line>.*)$', line)
        if m:
            commit_hash = m.group('commit_hash')
            author = m.group('author')
            datetime = m.group('datetime')
            date = m.group('date')
            time = m.group('time')
            timezone = m.group('timezone')
            line_number = int(m.group('line_number'))
            line = m.group('line')
            return LineBlame(commit_hash, author, datetime, line_number, line)
        else:
            print('Error: {}'.format(line))
        return None


if __name__ == '__main__':
    import doctest
    doctest.testmod()
