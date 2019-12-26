from day11 import execute


instructions = [
    "OR A J",
    "AND B J",
    "AND C J",
    "NOT J J",
    "AND D J",  # Up to here for part 1
    "OR E T",
    "OR H T",
    "AND T J",
    "RUN",
]


def generate_cmds():
    for instruction in instructions:
        for c in instruction:
            yield ord(c)
        yield 10


def run(program):
    out = pc = rb = 0
    cmds = generate_cmds()
    while out < 128:
        out, pc, rb = execute(program, cmds, pc, rb)
        if out == "HALT":
            return
        elif out >= 128:
            print(f"Damage: {out}")
            return
        elif out == 10:
            print()
        else:
            print(chr(out), end="")


if __name__ == "__main__":
    with open("../input/day21.txt") as f:
        program_text = f.readline()
    p = [int(val) for val in program_text.split(",")]
    run(p)
