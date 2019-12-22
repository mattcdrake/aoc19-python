import intcode
from helpers import prep_intcode_program
from itertools import permutations


phase_settings = list(permutations([0, 1, 2, 3, 4], 5))
max_thrust = -1

for amp_config in phase_settings:
    line_in = 0
    for amp in amp_config:
        pc = 0
        program = prep_intcode_program("./input/day7.txt")
        line_in, halt_type, pc = intcode.compute(program, [amp, line_in], pc)
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

        line_in, halt_type, pcs[amp_id] = intcode.compute(
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
