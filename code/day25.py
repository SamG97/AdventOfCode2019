import itertools
import sys

from day11 import execute


instructions = [
    "east",
    "take klein bottle",
    "east",
    "take semiconductor",
    "west",
    "north",
    "north",
    "north",
    "take dehydrated water",
    "south",
    "south",
    "south",
    "west",
    "north",
    "take sand",
    "north",
    "north",
    "take astrolabe",
    "south",
    "south",
    "west",
    "west",
    "take mutex",
    "east",
    "east",
    "south",
    "west",
    "north",
    "take shell",
    "south",
    "south",
    "west",
    "take ornament",
    "west",
    "south",
]


possible_items = [
    "klein bottle", "semiconductor", "dehydrated water", "sand", "astrolabe",
    "mutex", "shell", "ornament",
]


def user_input_generator():
    while True:
        user_input = input("> ")
        for c in user_input:
            yield ord(c)
        yield 10


def input_generator(cmds):
    for instruction in cmds:
        for c in instruction:
            yield ord(c)
        yield 10


def drop_generator(items):
    for item in items:
        command = f"drop {item}"
        for c in command:
            yield ord(c)
        yield 10
    for c in "south":
        yield ord(c)
    yield 10


if __name__ == "__main__":
    with open("../input/day25.txt") as f:
        program_text = f.readline()
    program = [int(val) for val in program_text.split(",")]
    pc = rb = 0
    gen = input_generator(instructions)
    buffer = ""
    checkpoint = False
    while True:
        out, pc, rb = execute(program, gen, pc, rb)
        if out == "HALT":
            break
        buffer += chr(out)
        if out == 10:
            if "Security Checkpoint" in buffer:
                checkpoint = True
            elif checkpoint and "Command" in buffer:
                break
            buffer = ""
    saved_program, saved_pc, saved_rb = program[:], pc, rb
    for num_to_drop in range(len(possible_items) + 1):
        for to_drop in itertools.combinations(possible_items, num_to_drop):
            program, pc, rb = saved_program[:], saved_pc, saved_rb
            gen = drop_generator(to_drop)
            failed = False
            saved_buffer = ""
            track_buffer = False
            while True:
                out, pc, rb = execute(program, gen, pc, rb)
                if out == "HALT":
                    break
                buffer += chr(out)
                if out == 10:
                    if "Alert" in buffer:
                        failed = True
                    elif failed and "Command" in buffer:
                        break
                    elif "Analyzing..." in buffer:
                        track_buffer = True
                    if track_buffer:
                        saved_buffer += buffer
                    buffer = ""
            if not failed:
                print(saved_buffer)
                sys.exit(0)
