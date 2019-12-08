# Clean file input and return a list of program instructions
def prep_day_2(path):
    with open(path) as f:
        instructions = f.readlines()
    instructions = str.split(instructions[0], ",")
    instructions = list(map(int, instructions))
    return instructions


def compute(program, noun, verb):
    program[1] = noun
    program[2] = verb
    pc = 0
    opcode = program[pc]

    while opcode != 99:
        # Pull values from memory
        arg1 = program[program[pc+1]]
        arg2 = program[program[pc+2]]

        if opcode == 1:
            result = arg1 + arg2
        else:
            result = arg1 * arg2

        program[program[pc+3]] = result
        pc += 4
        opcode = program[pc]

    return program[0]


def part_two():
    for i in range(0, 99):
        for j in range(0, 99):
            if compute(program.copy(), i, j) == 19690720:
                return 100 * i + j


program = prep_day_2("input/day2.txt")
print("part 1: " + str(compute(program.copy(), 12, 2)))
print("part 2: " + str(part_two()))

