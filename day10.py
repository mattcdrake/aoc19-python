from pprint import pprint
from fractions import Fraction as frac
from math import atan2, degrees, sqrt
from sys import maxsize


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


def sort_asteroids(value):
    return value[0]


def get_tiebreaker_index(distances, eligibles, deleted):
    min_distance = maxsize
    min_index = 0
    for index, candidate in enumerate(eligibles):
        if distances[candidate][1] < min_distance:
            min_index = index
    return eligibles[min_index]


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

max_obs = max(asteroid_obs.values())
print("part 1: " + str(max_obs))

for k, v in asteroid_obs.items():
    if v == max_obs:
        laser = k

distances = []
for asteroid in asteroid_positions:
    if laser == asteroid:
        continue
    # Backwards because the y-axis is flipped
    opp = laser[1] - asteroid[1]
    adj = asteroid[0] - laser[0]
    angle = degrees(atan2(opp, adj)) % 360
    angle = (angle - 90) % 360
    if angle == 0:
        angle = 360
    distance = sqrt(pow(opp, 2) + pow(adj, 2))
    distances.append([angle, distance, asteroid])

distances.sort(reverse=True, key=sort_asteroids)

deleted = []
i = 0
while i < len(distances):
    eligibles = [i]
    angle = distances[i][0]
    i += 1
    while i < len(distances) and distances[i][0] == angle:
        eligibles.append(i)
        i += 1
    if len(eligibles) > 1:
        deletion_index = get_tiebreaker_index(distances, eligibles, deleted)
    else:
        deletion_index = eligibles[0]
    deleted.append(distances[deletion_index])
    del distances[deletion_index]
    i -= 1
    if i >= (len(distances) - 1):
        i = 0

target = deleted[199][2]
print("part 2: " + str(target[0] * 100 + target[1]))
