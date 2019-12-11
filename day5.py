from helpers import prep_intcode_program

def get_opcode(value):
    return value % 100


# Chop off the opcode and return a list of the parameter mode values. Pads the
# list with 0 for parameter modes.
def get_param_modes(value):
    if value < 100:
        return [0, 0, 0]
    value = value // 100
    param_modes = [int(i) for i in str(value)]
    while len(param_modes) < 3:
        param_modes.insert(0, 0)
    return param_modes


# Returns a list of 3 arguments that have been processed according to parameter
# mode rules.
def parse_args(program, opcode, pc, param_modes):
    args = [0, 0, 0]
    
    # Opcodes w/ 1 arg
    if opcode == 3:
        args[0] = program[pc+1]
    elif opcode == 4:
        if param_modes[2] == 0:
            args[0] = program[program[pc+1]]
        else:
            args[0] = program[pc+1]
    # Opcodes w/ 2 args
    elif opcode in (5, 6):
        args[0] = program[program[pc+1]] if param_modes[2] == 0 else program[pc+1]
        args[1] = program[program[pc+2]] if param_modes[1] == 0 else program[pc+2]
    # Opcodes w/ 3 args
    elif opcode in (1, 2, 7, 8):
        args[0] = program[program[pc+1]] if param_modes[2] == 0 else program[pc+1]
        args[1] = program[program[pc+2]] if param_modes[1] == 0 else program[pc+2]
        args[2] = program[pc+3]
    
    return args


def compute(program, input):
    pc = 0
    opcode_raw = program[pc]
    opcode = get_opcode(opcode_raw)
    param_modes = get_param_modes(opcode_raw)

    while opcode != 99:
        args = parse_args(program, opcode, pc, param_modes)
        # Execute opcode
        if opcode == 1:
            program[args[2]] = args[0] + args[1]
            pc += 4
        elif opcode == 2:
            program[args[2]] = args[0] * args[1]
            pc += 4
        elif opcode == 3:
            program[args[0]] = input
            pc += 2
        elif opcode == 4:
            print(args[0])
            pc += 2
        elif opcode == 5:
            if args[0] != 0:
                pc = args[1]
            else:
                pc += 3
        elif opcode == 6:
            if args[0] == 0:
                pc = args[1]
            else:
                pc += 3
        elif opcode == 7:
            if args[0] < args[1]:
                program[args[2]] = 1
            else:
                program[args[2]] = 0
            pc += 4
        elif opcode == 8:
            if args[0] == args[1]:
                program[args[2]] = 1
            else:
                program[args[2]] = 0
            pc += 4

        # Get new opcodes
        opcode_raw = program[pc]
        opcode = get_opcode(opcode_raw)
        param_modes = get_param_modes(opcode_raw)

    return program[0]


program = prep_intcode_program("./input/day5.txt")
compute(program, 1)
program = prep_intcode_program("./input/day5.txt")
compute(program, 5)
