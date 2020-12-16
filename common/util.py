def solution(filename, function, parser):
    with open(f"data/{filename}") as f:
        return function(parser(f))


def split_parser(file):
    return file.read().split()


def line_parser(file):
    return file.read().splitlines()
