from helpers import prep_intcode_program
from itertools import permutations


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
    # Opcodes w/ 2 or 3 args
    elif opcode in (1, 2, 5, 6, 7, 8):
        args[0] = program[program[pc+1]] if param_modes[2] == 0 else program[pc+1]
        args[1] = program[program[pc+2]] if param_modes[1] == 0 else program[pc+2]
        # Opcodes w/ 3 args
        if opcode in (1, 2, 7, 8):
            args[2] = program[pc+3]

    return args


def compute(program, inputs, pc):
    cur_input = 0
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
        # Input instruction
        elif opcode == 3:
            program[args[0]] = inputs[cur_input]
            cur_input += 1
            pc += 2
        # Output instruction
        elif opcode == 4:
            pc += 2
            return(args[0], "output", pc)
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

    return (program[0], "halt", pc)


phase_settings = list(permutations([0, 1, 2, 3, 4], 5))
max_thrust = -1

for amp_config in phase_settings:
    line_in = 0
    for amp in amp_config:
        pc = 0
        program = prep_intcode_program("./input/day7.txt")
        line_in, halt_type, pc = compute(program, [amp, line_in], pc)
        line_in = line_in
    if line_in > max_thrust:
        max_thrust = line_in

print("part 1: " + str(max_thrust))

phase_settings = list(permutations([5, 6, 7, 8, 9], 5))
max_thrust = -1

for amp_config in phase_settings:
    first_run = True
    found = False
    programs = [prep_intcode_program("./input/day7.txt")
                for i in range(0, 5)]
    pcs = [0, 0, 0, 0, 0]
    amp_id = 0
    last_e_signal = -1
    line_in = 0

    while not found or amp_id != 0:
        if first_run:
            line_in = [amp_config[amp_id], line_in]
        else:
            line_in = [line_in]

        line_in, halt_type, pcs[amp_id] = compute(
            programs[amp_id], line_in, pcs[amp_id])

        if halt_type == "output" and amp_id == 4:
            last_e_signal = line_in

        if halt_type == "halt":
            found = True

        if amp_id == 4:
            first_run = False

        amp_id = (amp_id + 1) % 5

    if last_e_signal > max_thrust:
        max_thrust = last_e_signal

print("part 2: " + str(max_thrust))
