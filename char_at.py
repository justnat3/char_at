#!/usr/bin/python3
import sys
import os
from typing import Union

RED = "\033[91m"
RESET = "\033[0m"

def process_around_read(buff: str, position: int) -> tuple:
    # position is already ensured to be int, not mutated in the last scope

    line_num = 0
    collect = []
    result = []

    buff_cpy = buff[:position]
    line_num = buff_cpy.count("\n")

    # copy position
    ptr = position

    # read backwards until we find a \n
    while ptr > 1:
        # starting at the position go backwards
        collect.append(buff[ptr])
        if buff[ptr] == "\n":
            break
        ptr -= 1

    # append the collected chars into the result as list()
    # then reset the collector
    result.append(collect)
    collect = []

    # copy the position back into ptr
    ptr = position

    # read forward until we find a \n
    while ptr < len(buff)-1:
        # starting at the position go forward 
        collect.append(buff[ptr])
        if buff[ptr] == "\n":
            break
        ptr += 1


    result.append("\n")
    result.append("Error found here", " "*ptr-2, "^") # pyright: ignore
    result.append(collect)
    copy = ""

    for li in result:
        copy += ''.join(li).strip("\n")
        copy = copy[::-1]

    return copy, line_num


def char_in_file(file: str, position: int, read_around: bool) -> Union[str, None]:
    result = "Found Nothing"
    buff = ""
    found = None
    count = None

    assert isinstance(position, int), "position is not a int"
    with open(file, 'r') as fd:
        try:
            buff = fd.read()
        except Exception as e:
            print("[ERROR] Unable to read file", e)

        try:
            result = buff[position-1]

            if read_around:
                found, count = process_around_read(buff, position)

            print("line number:",count)
            result = found


        except Exception as err:
            print("[ERROR] read out of bounds")
            raise err

    return result


def print_usage():
    print("[USAGE] ./char_at [FILE] [POSITION_IN_FILE] {--read_around}")

if __name__ == "__main__":
    read_around = False

    if len(sys.argv) <= 2:
        print_usage()
        sys.exit(1)

    # where argv[0] is the program name
    file = sys.argv[1]
    position = int(sys.argv[2])
    if not os.path.exists(file):
        print("[ERROR] File does not exist")
        print_usage()
        sys.exit(1)

    if '--read-around' in sys.argv:
        read_around = True

    found = char_in_file(file, position, read_around)
    print(found)

    sys.exit(0)
