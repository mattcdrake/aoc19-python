# Clean file input and return a list of program instructions
def prep_intcode_program(path):
    with open(path) as f:
        instructions = f.readlines()
    instructions = str.split(instructions[0], ",")
    instructions = list(map(int, instructions))
    return instructions
