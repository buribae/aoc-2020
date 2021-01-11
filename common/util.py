def solution(filename, function, parser):
    return function(get_data(filename, parser))


def split_parser(data):
    return data.split()


def line_parser(data):
    return data.splitlines()


def int_parser(data):
    return [int(i) for i in data.splitlines()]


def grid_parser(data):
    return [[coord for coord in line] for line in data.splitlines()]


def get_data(filename, parser):
    with open(f"data/{filename}") as f:
        return parser(f.read())
