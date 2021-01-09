def solution(filename, function, parser):
    return function(get_data(filename, parser))


def split_parser(file):
    return file.read().split()


def line_parser(file):
    return file.read().splitlines()


def int_parser(file):
    return [int(i) for i in file.read().splitlines()]


def get_data(filename, parser):
    with open(f"data/{filename}") as f:
        return parser(f)
