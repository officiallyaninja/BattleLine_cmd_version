from typing import List
from custom_errors import NoValidOptionsError


def get_int_in_list(valid_ints: List[int], msg: str = ""):
    if len(valid_ints) == 0:
        raise NoValidOptionsError()

    while True:
        try:
            num = int(input(msg))
        except ValueError:
            print("ERR: Not a number")
            continue
        if num in valid_ints:
            return num
        else:
            print(f"ERR: num should be one of {valid_ints}")
            continue


def get_int_in_range(min: int, max: int, msg: str = 0):
    """half open range, min is inclusive, max is exclusive"""
    if max <= min:
        raise NoValidOptionsError(f"max({max}) is bigger than min({min})")
    return get_int_in_list([i for i in range(min, max)], msg)