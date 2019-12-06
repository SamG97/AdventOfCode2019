def execute(program):
    pc = 0
    while True:
        instruction = [c for c in str(program[pc])]
        while len(instruction) < 5:
            instruction.insert(0, "0")
        # print(pc, instruction)
        # print(program[225])
        opcode = int(instruction[-2] + instruction[-1])

        if opcode == 99:
            return program

        immediate_1 = instruction[2] == "1"
        immediate_2 = instruction[1] == "1"
        # immediate_3 never set
        
        if immediate_1:
            left = program[pc + 1]
        else:
            left = program[program[pc + 1]]
        if opcode != 3 and opcode != 4:
            if immediate_2:
                right = program[pc + 2]
            else:
                right = program[program[pc + 2]]
            res = program[pc + 3]
        if opcode == 1:  # Plus
            program[res] = left + right
        elif opcode == 2:  # Multiply
            program[res] = left * right
        elif opcode == 3:  # Input
            program[program[pc + 1]] = int(input("> "))
        elif opcode == 4:  # Output
            print(left)
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
            program[res] = 1 if left < right else 0
        elif opcode == 8:  # Equals
            program[res] = 1 if left == right else 0
        else:
            raise RuntimeError(f"Unknown opcode {opcode} at pc {pc}")
        
        if opcode in [1, 2, 7, 8]:
            pc += 4
        elif opcode == 3 or opcode == 4:
            pc += 2

if __name__ == "__main__":
    with open("../input/day5.txt") as f:
        program_text = f.readline()
    program = [int(val) for val in program_text.split(",")]
    execute(program)
