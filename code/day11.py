from collections import defaultdict
import numpy as np
from matplotlib import pyplot as plt


def execute(program, inputs, pc=0, relative_base=0):
    def read_addr(addr):
        while addr > len(program) - 1:
            program.append(0)
        return program[addr]

    def write_addr(addr, value):
        while addr > len(program) - 1:
            program.append(0)
        program[addr] = value

    if type(inputs) in [list, tuple]:
        inputs = iter(inputs)

    while True:
        instruction = [c for c in str(program[pc])]
        while len(instruction) < 5:
            instruction.insert(0, "0")
        opcode = int(instruction[-2] + instruction[-1])

        if opcode == 99:
            return "HALT", pc, relative_base

        immediate_1 = int(instruction[2])
        immediate_2 = int(instruction[1])
        immediate_3 = int(instruction[0])

        if immediate_1 == 1:
            left = read_addr(pc + 1)
        elif immediate_1 == 2:
            left = read_addr(relative_base + read_addr(pc + 1))
        else:
            left = read_addr(read_addr(pc + 1))
        if not opcode in [3, 4, 9]:
            if immediate_2 == 1:
                right = read_addr(pc + 2)
            elif immediate_2 == 2:
                right = read_addr(relative_base + read_addr(pc + 2))
            else:
                right = read_addr(read_addr(pc + 2))
            if immediate_3 == 2:
                res = relative_base + read_addr(pc + 3)
            else:
                res = read_addr(pc + 3)
        if opcode == 1:  # Plus
            write_addr(res, left + right)
        elif opcode == 2:  # Multiply
            write_addr(res, left * right)
        elif opcode == 3:  # Input
            if immediate_1 == 2:
                addr = relative_base + read_addr(pc + 1)
            else:
                addr = read_addr(pc + 1)
            indata = next(inputs)
            write_addr(addr, indata)
        elif opcode == 4:  # Output
            return left, pc + 2, relative_base
        elif opcode == 5:  # Branch if true
            if left != 0:
                pc = right
            else:
                pc += 3
        elif opcode == 6:  # Branch if false
            if left == 0:
                pc = right
            else:
                pc += 3
        elif opcode == 7:  # Less than
            write_addr(res, 1 if left < right else 0)
        elif opcode == 8:  # Equals
            write_addr(res, 1 if left == right else 0)
        elif opcode == 9:  # Update relative base
            relative_base += left
        else:
            raise RuntimeError(f"Unknown opcode {opcode} at pc {pc}")
        
        if opcode in [1, 2, 7, 8]:
            pc += 4
        elif opcode in [3, 4, 9]:
            pc += 2


if __name__ == "__main__":
    with open("../input/day11.txt") as f:
        program_text = f.readline()
    program = [int(val) for val in program_text.split(",")]
    grid = defaultdict(lambda: ".")
    pos = (0, 0)
    grid[pos] = "#"
    direction = 0
    pc = 0
    rb = 0
    while True:
        current_val = 1 if grid[pos] == "#" else 0
        colour, pc, rb = execute(program, [current_val], pc, rb)
        grid[pos] = "#" if colour else "."
        turn, pc, rb = execute(program, [], pc, rb)
        if turn == 0:
            direction = (direction - 1) % 4
        elif turn == 1:
            direction = (direction + 1) % 4
        elif turn == "HALT":
            break
        else:
            raise ValueError(f"Unknown direction {turn}")
        
        if direction == 0:
            pos = (pos[0], pos[1] - 1)
        elif direction == 1:
            pos = (pos[0] + 1, pos[1])
        elif direction == 2:
            pos = (pos[0], pos[1] + 1)
        else:
            pos = (pos[0] - 1, pos[1])
    xs, ys = zip(*grid.keys())
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    data = np.zeros((max_y - min_y + 1, max_x - min_x + 1, 3), dtype=np.uint8)
    for i, y in enumerate(range(min(ys), max(ys) + 1)):
        for j, x in enumerate(range(min(xs), max(xs) + 1)):
            if grid[(x, y)] == "#":
                data[i, j] = [255] * 3
    plt.imshow(data, interpolation='nearest')
    plt.show()
    
