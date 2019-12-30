from intcode import IntcodeComputer
from helpers import prep_intcode_program
from fractions import Fraction


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


def find_tile(screen, tile):
    x = -1
    y = -1
    for index_y, row in enumerate(screen):
        for index_x, col in enumerate(row):
            if col == tile:
                x = index_x
                y = index_y
    return (x, y)


def update_joystick(ball, paddle):
    if paddle[0] > ball[0]:
        return -1
    elif paddle[0] < ball[0]:
        return 1
    else:
        return 0


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

print("part 1: " + str(count_tiles(screen, 2)))

program = prep_intcode_program("./input/day13_2.txt")
computer = IntcodeComputer(program.copy())
screen = [[0]]
score = 0
joystick = 0
output = ("dummy", "dummy")
while output[1] != "halt":
    x = computer.compute([joystick])[0]
    y = computer.compute([joystick])[0]
    output = computer.compute([joystick])
    if x == -1 and y == 0:
        score = output[0]
    else:
        check_bounds(screen, x, y)
        place_tile(screen, x, y, output[0])

    ball = find_tile(screen, 4)
    paddle = find_tile(screen, 3)
    if ball[0] != -1 and paddle[0] != -1:
        joystick = update_joystick(ball, paddle)

print("part 2: " + str(score))
