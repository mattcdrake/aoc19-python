from data.CordSegment import CordSegment
from sys import maxsize

# Returns a list of lists, one for each cord. The inner lists are comprised of
# CordSegments.
def prep_day_3(path):
    with open(path) as f:
        cords = f.readlines()
    output = []
    for cord in cords:
        segments = cord.split(",")
        clean_segments = []
        for segment in segments:
            direction = segment[0]
            distance = int(segment[1:])
            clean_segments.append(CordSegment(direction, distance))
        output.append(clean_segments)
    return output


def update_board(cord_id, board, key, steps):
    if (key in board) and (cord_id not in board[key]):
        board[key][cord_id] = steps
    else:
        board[key] = {cord_id: steps}


def process_right(cord_id, board, x, y, distance, steps):
    while distance > 0:
        square = str(x) + "," + str(y)
        update_board(cord_id, board, square, steps)
        x += 1
        distance -= 1
        steps += 1


def process_left(cord_id, board, x, y, distance, steps):
    while distance > 0:
        square = str(x) + "," + str(y)
        update_board(cord_id, board, square, steps)
        x -= 1
        distance -= 1
        steps += 1


def process_up(cord_id, board, x, y, distance, steps):
    while distance > 0:
        square = str(x) + "," + str(y)
        update_board(cord_id, board, square, steps)
        y -= 1
        distance -= 1
        steps += 1


def process_down(cord_id, board, x, y, distance, steps):
    while distance > 0:
        square = str(x) + "," + str(y)
        update_board(cord_id, board, square, steps)
        y += 1
        distance -= 1
        steps += 1


def calc_manhattan_dist(coordinates):
    coordinates = list(map(int, coordinates.split(",")))
    return abs(coordinates[0]) + abs(coordinates[1])


cords = prep_day_3("./input/day3.txt")
board = {}

# At this point, board is a dictionary where the key is a string of the form 
# "x,y" and the values are the IDs of the cords that pass through that square.
cord_id = 0
for cord in cords:
    x_pos = 0
    y_pos = 0
    steps = 0
    for segment in cord:
        if segment.direction == "L":
            process_left(cord_id, board, x_pos, y_pos, segment.distance, steps)
            x_pos -= segment.distance
        elif segment.direction == "U":
            process_up(cord_id, board, x_pos, y_pos, segment.distance, steps)
            y_pos -= segment.distance
        elif segment.direction == "R":
            process_right(cord_id, board, x_pos, y_pos, segment.distance, steps)
            x_pos += segment.distance
        elif segment.direction == "D":
            process_down(cord_id, board, x_pos, y_pos, segment.distance, steps)
            y_pos += segment.distance
        steps += segment.distance
    cord_id += 1

min_distance = maxsize
min_steps = maxsize

for key, value in board.items():
    if len(value) > 1:
        manhattan_distance = calc_manhattan_dist(key)
        if manhattan_distance < min_distance and manhattan_distance != 0:
            min_distance = manhattan_distance

        # value here has the form {0: 120230, 1: 21387}
        current_steps = 0
        for cord_id, steps in value.items():
            current_steps += steps
        
        if current_steps < min_steps and manhattan_distance != 0:
            min_steps = current_steps


print("part 1: " + str(min_distance))
print("part 2: " + str(min_steps))
