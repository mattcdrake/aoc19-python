from intcode import IntcodeComputer
from helpers import prep_intcode_program


def check_bounds(screen, x, y):
    diff = y - len(screen) + 1
    if diff > 0:
        for i in range(diff):
            screen.append([0 for i in range(len(screen[0]))])
    diff = x - len(screen[0]) + 1
    if diff > 0:
        for row in screen:
            row.extend([0 for i in range(diff)])


def place_tile(screen, x, y, tile):
    screen[y][x] = tile


def count_tiles(screen, tile):
    total = 0
    for row in screen:
        for col in row:
            if col == tile:
                total += 1
    return total


def print_screen(screen):
    for row in screen:
        for col in row:
            print(col, end="")
        print()


program = prep_intcode_program("./input/day13_1.txt")
computer = IntcodeComputer(program.copy())
screen = [[0]]
output = ("dummy", "dummy")
while output[1] != "halt":
    x = computer.compute([])[0]
    y = computer.compute([])[0]
    check_bounds(screen, x, y)
    output = computer.compute([])
    place_tile(screen, x, y, output[0])

print_screen(screen)
print("part 1: " + str(count_tiles(screen, 2)))
