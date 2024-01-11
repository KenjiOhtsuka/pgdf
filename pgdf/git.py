import os
import subprocess


def get_label() -> str:
    result = subprocess.run(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(result.stderr.decode('utf-8'))
        exit(result.returncode)
    path = result.stdout.decode('utf-8')
    path = path.strip()
    return os.path.basename(path)


def get_summary(revision_1: str, revision_2: str) -> str:
    result = subprocess.run(['git', 'diff', '--stat=200', revision_1, revision_2], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(result.stderr.decode('utf-8'))
        exit(result.returncode)
    result_text = result.stdout.decode('utf-8')
    return result_text


def get_diff(revision_1: str, revision_2: str) -> str:
    result = subprocess.run(['git', 'diff', revision_1, revision_2], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(result.stderr.decode('utf-8'))
        exit(result.returncode)
    result_text = result.stdout.decode('utf-8')
    return result_text


def get_blame(revision: str, file_path: str, start_line_number: int, volume: int) -> str:
    result = subprocess.run(['git', 'blame', '-L', f'{start_line_number},+{volume}', revision, '--', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(result.stderr.decode('utf-8'))
        exit(result.returncode)
    result_text = result.stdout.decode('utf-8')
    return result_text
