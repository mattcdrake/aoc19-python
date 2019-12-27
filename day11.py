from helpers import prep_intcode_program
from intcode import IntcodeComputer

# Direction (x, y) follows shape of 2d list. -y moves up, -x moves left
# Up: (0, -1)
# Right: (1, 0)
# Down: (0, 1)
# Left: (-1, 0)


class Robot:
    def __init__(self):
        self.pos = (0, 0)
        self.direction = (0, -1)

    def turn_right(self):
        if self.direction == (0, -1):
            self.direction = (1, 0)
        elif self.direction == (1, 0):
            self.direction = (0, 1)
        elif self.direction == (0, 1):
            self.direction = (-1, 0)
        else:
            self.direction = (0, -1)

    def turn_left(self):
        if self.direction == (0, -1):
            self.direction = (-1, 0)
        elif self.direction == (-1, 0):
            self.direction = (0, 1)
        elif self.direction == (0, 1):
            self.direction = (1, 0)
        else:
            self.direction = (0, -1)

    def get_next_pos(self):
        new_pos_x = self.pos[0] + self.direction[0]
        new_pos_y = self.pos[1] + self.direction[1]
        return (new_pos_x, new_pos_y)

    def move(self):
        self.pos = self.get_next_pos()

    def shift_pos(self, direction):
        if direction == "right":
            new_pos_x = self.pos[0] + 1
            self.pos = (new_pos_x, self.pos[1])
        elif direction == "down":
            new_pos_y = self.pos[1] + 1
            self.pos = (self.pos[0], new_pos_y)


def check_hull_size(hull, robot):
    next_pos = robot.get_next_pos()
    if next_pos[0] < 0:
        for row in hull:
            row.insert(0, 0)
        robot.shift_pos("right")
        return (True, "right")
    if next_pos[0] > len(hull[0]) - 1:
        for row in hull:
            row.append(0)
    if next_pos[1] < 0:
        hull.insert(0, [0 for i in range(0, len(hull[0]))])
        robot.shift_pos("down")
        return (True, "down")
    if next_pos[1] > len(hull) - 1:
        hull.append([0 for i in range(0, len(hull[0]))])
    return (False, "dummy")


def shift_painted_squares(painted_squares, direction):
    new_painted_squares = []
    for square in painted_squares:
        if direction == "right":
            new_painted_squares.append((square[0]+1, square[1]))
        elif direction == "down":
            new_painted_squares.append((square[0], square[1]+1))
    return new_painted_squares


def get_current_color(hull, robot):
    return hull[robot.pos[1]][robot.pos[0]]


def paint_square(hull, robot, color, painted_squares):
    x = robot.pos[0]
    y = robot.pos[1]
    hull[y][x] = color
    if (x, y) not in painted_squares:
        painted_squares.append((x, y))


program = prep_intcode_program("./input/day11.txt")
computer = IntcodeComputer(program.copy())
robot = Robot()
hull = [[0]]
painted_squares = []
output = ("dummy", "dummy")
while output[1] != "halt":
    next_color = computer.compute([get_current_color(hull, robot)])[0]
    paint_square(hull, robot, next_color, painted_squares)
    output = computer.compute([])
    next_turn = output[0]
    if next_turn == 0:
        robot.turn_left()
    else:
        robot.turn_right()
    shifted = check_hull_size(hull, robot)
    if shifted[0]:
        painted_squares = shift_painted_squares(painted_squares, shifted[1])
    robot.move()


print("part 1: " + str(len(painted_squares)))

program = prep_intcode_program("./input/day11.txt")
computer = IntcodeComputer(program.copy())
robot = Robot()
hull = [[1]]
painted_squares = []
output = ("dummy", "dummy")
while output[1] != "halt":
    next_color = computer.compute([get_current_color(hull, robot)])[0]
    paint_square(hull, robot, next_color, painted_squares)
    output = computer.compute([])
    next_turn = output[0]
    if next_turn == 0:
        robot.turn_left()
    else:
        robot.turn_right()
    shifted = check_hull_size(hull, robot)
    if shifted[0]:
        painted_squares = shift_painted_squares(painted_squares, shifted[1])
    robot.move()

print("part 2: ")
for row in hull:
    print(row)
