
def get_num(string):
    new_string = string.replace(",", "")
    return new_string[:-1]


def clear_param(string):
    return string[1:]