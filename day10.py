from pprint import pprint
from fractions import Fraction as frac


def prep_input(path):
    with open(path) as f:
        lines = f.readlines()
    asteroids = []
    y = 0
    for line in lines:
        line = line.strip()
        asteroids.append([])
        for char in line:
            asteroids[y].append(char)
        y += 1
    return asteroids


def log_asteroids(asteroids):
    asteroid_positions = []
    for y, row in enumerate(asteroids):
        for x, col in enumerate(row):
            if col == "#":
                asteroid_positions.append((x, y))
    return asteroid_positions


# From candidate to destination
def get_vector(candidate, destination):
    x = candidate[0] - destination[0]
    y = candidate[1] - destination[1]
    x_sign = 1 if x >= 0 else -1
    y_sign = 1 if y >= 0 else -1

    if y == 0:
        output = (x_sign, 0)
    elif x == 0:
        output = (0, y_sign)
    else:
        vector = frac(x, y)
        x = x_sign * abs(vector.numerator)
        y = y_sign * abs(vector.denominator)
        output = (x, y)
    return output


def is_observable(asteroids, candidate, destination):
    vector = get_vector(candidate, destination)
    dest_x = destination[0] + vector[0]
    dest_y = destination[1] + vector[1]
    while (dest_x, dest_y) != candidate:
        if asteroids[dest_y][dest_x] == "#":
            return False
        dest_x += vector[0]
        dest_y += vector[1]
    return True


# Count total asteroids
asteroids = prep_input("./input/day10.txt")
asteroid_positions = log_asteroids(asteroids)

# For each asteroid, count the number of asteroids that are blocked from view.
asteroid_obs = {}
for candidate in asteroid_positions:
    observable = 0
    for destination in asteroid_positions:
        if candidate == destination:
            continue
        if is_observable(asteroids, candidate, destination):
            observable += 1
    asteroid_obs[candidate] = observable

print("part 1: " + str(max(asteroid_obs.values())))
