def read_data(filename, function, split_char=None):
    with open(f"data/{filename}") as f:
        return function(f.read().split(split_char))

