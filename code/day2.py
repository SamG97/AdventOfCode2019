def execute(program):
    pc = 0
    while True:
        opcode = program[pc]
        if opcode == 99:
            return program
        
        left = program[program[pc + 1]]
        right = program[program[pc + 2]]
        if opcode == 1:
            program[program[pc + 3]] = left + right
        elif opcode == 2:
            program[program[pc + 3]] = left * right
        else:
            raise RuntimeError(f"Unknown opcode {opcode}")
        
        pc += 4

if __name__ == "__main__":
    with open("../input/day2.txt") as f:
        program_text = f.readline()
    for noun in range(100):
        for verb in range(100):
            program = [int(val) for val in program_text.split(",")]
            program[1] = noun
            program[2] = verb
            res = execute(program)[0]
            if res == 19690720:
                print(noun, verb)
                print(noun * 100 + verb)
                exit(0)