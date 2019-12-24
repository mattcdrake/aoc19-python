from helpers import prep_intcode_program
from intcode import IntcodeComputer

program = prep_intcode_program("./input/day9.txt")
computer = IntcodeComputer(program.copy())
output, code = computer.compute([1])
print("part 1: " + str(output))
computer = IntcodeComputer(program.copy())
output, code = computer.compute([2])
print("part 2: " + str(output))
