import numpy as np
import itertools

from day11 import execute


def render_grid(program):
    pc = rb = 0
    rows = []
    row = []
    while True:
        out, pc, rb = execute(program, [], pc, rb)
        if out == "HALT":
            if row:
                print("Adding final row")
                rows.append(row)
            break
        elif out == 10:
            if row:
                rows.append(row)
                row = []
        else:
            row.append(chr(out))
    return np.array(rows).transpose((1, 0))


def find_alignment_sum(grid):
    def is_intersection(i, j):
        for offset in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
            if grid[i + offset[0], j + offset[1]] == ".":
                return False
        return True

    x_lim, y_lim = grid.shape
    total = 0
    for x in range(1, x_lim - 1):
        for y in range(1, y_lim - 1):
            if is_intersection(x, y):
                total += x * y
    return total


directions = (
    np.array([0, -1]), np.array([1, 0]), np.array([0, 1]), np.array([-1, 0])
)


def find_path(grid):
    def get_elem(coords):
        if 0 <= coords[0] < x_max and 0 <= coords[1] < y_max:
            return grid[coords[0], coords[1]]
        else:
            return "."

    grid = grid.copy()
    x_max, y_max = grid.shape
    pos = np.argwhere(grid == "^")[0]
    direction = 0
    instructions = []
    while "#" in grid:
        right_dir = (direction + 1) % 4
        right_pos = pos + directions[right_dir]
        if get_elem(right_pos) == "#":
            direction = right_dir
            pos = right_pos
            instructions.append("R")
        else:
            direction = (direction - 1) % 4
            pos = pos + directions[direction]
            assert get_elem(pos) == "#"
            instructions.append("L")
        forward_moves = 0
        while get_elem(pos) != ".":
            grid[pos[0], pos[1]] = "O"
            forward_moves += 1
            pos += directions[direction]
        pos -= directions[direction]
        instructions.append(str(forward_moves))
    return instructions


def reduce_instructions(instructions):
    def reduce_string(fst, snd, thrd):
        replaced_string = full_string.replace(fst, "A")
        replaced_string = replaced_string.replace(snd, "B")
        replaced_string = replaced_string.replace(thrd, "C")
        return replaced_string

    def count_errors(fst, snd, thrd):
        replaced_string = reduce_string(fst, snd, thrd)
        errors = 0
        for char in replaced_string:
            if char not in ["A", "B", "C", ","]:
                errors += 1
        return errors

    full_string = ",".join(instructions)
    substrings = []
    for start in range(0, len(instructions) - 4, 2):
        for end in range(start + 4, min(start + 10, len(instructions)), 2):
            string = ",".join(instructions[start:end])
            if len(string) > 20:
                continue
            cnt = full_string.count(string)
            if cnt > 1:
                substrings.append(string)
    for a, b, c in itertools.combinations(substrings, 3):
        if count_errors(a, b, c) == 0:
            return reduce_string(a, b, c), a, b, c, "N"


def rescue_bots(program, instructions):
    program[0] = 2
    cmds = iter([ord(c) for p in instructions for c in p + "\n"])
    idx = pc = rb = out = 0
    while out < 128:
        idx += 1
        out, pc, rb = execute(program, cmds, pc, rb)
    return out


if __name__ == "__main__":
    with open("../input/day17.txt") as f:
        program_text = f.readline()
    p = [int(val) for val in program_text.split(",")]
    g = render_grid(p[:])
    path = find_path(g)
    instrs = reduce_instructions(path)
    print(rescue_bots(p, instrs))
