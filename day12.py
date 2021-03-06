from numpy import lcm


class Body:
    # Position {'x': n, 'y': n, 'z': n}
    def __init__(self, position):
        self.initial_pos = position.copy()
        self.position = position
        self.velocity = {'x': 0, 'y': 0, 'z': 0}

    def update_velocity(self, velocity):
        self.velocity['x'] += velocity['x']
        self.velocity['y'] += velocity['y']
        self.velocity['z'] += velocity['z']

    def update_position(self):
        self.position['x'] += self.velocity['x']
        self.position['y'] += self.velocity['y']
        self.position['z'] += self.velocity['z']


def find_velocity_delta(body1, body2):
    if body1 == body2:
        return (0, 0)
    elif body1 > body2:
        return (-1, 1)
    else:
        return (1, -1)


def update_velocities(body1, body2):
    x = find_velocity_delta(body1.position['x'], body2.position['x'])
    y = find_velocity_delta(body1.position['y'], body2.position['y'])
    z = find_velocity_delta(body1.position['z'], body2.position['z'])
    body1.update_velocity({'x': x[0], 'y': y[0], 'z': z[0]})
    body2.update_velocity({'x': x[1], 'y': y[1], 'z': z[1]})


def advance_time(bodies):
    for i in range(0, len(bodies)):
        for j in range(i+1, len(bodies)):
            update_velocities(bodies[i], bodies[j])

    for body in bodies:
        body.update_position()


def parse_coordinate(string, coordinate):
    start = string.find(coordinate) + 2
    comma = string.find(",", start)
    tag = string.find(">", start)
    end = comma if comma < tag else tag
    val = string[start:end]
    return val


def parse_input(path):
    bodies = []
    with open(path) as f:
        for line in f.readlines():
            line = line.strip()
            x = int(parse_coordinate(line, "x"))
            y = int(parse_coordinate(line, "y"))
            z = int(parse_coordinate(line, "z"))
            body = Body({'x': x, 'y': y, 'z': z})
            bodies.append(body)
    return bodies


def find_potential_energy(body):
    x = abs(body.position['x'])
    y = abs(body.position['y'])
    z = abs(body.position['z'])
    return x + y + z


def find_kinetic_energy(body):
    x = abs(body.velocity['x'])
    y = abs(body.velocity['y'])
    z = abs(body.velocity['z'])
    return x + y + z


def find_energy(bodies):
    total_energy = 0
    for body in bodies:
        pot = find_potential_energy(body)
        kin = find_kinetic_energy(body)
        total_energy += pot * kin
    return total_energy


def found_all_steps(steps):
    for i in range(3):
        if steps[i] < 0:
            return False
    return True


def is_same_state(bodies, axis):
    found = []
    for i in range(4):
        same_pos = bodies[i].position[axis] == bodies[i].initial_pos[axis]
        same_vel = bodies[i].velocity[axis] == 0
        found.append(same_pos and same_vel)
    return all(found)


bodies = parse_input("./input/day12.txt")

for i in range(0, 1000):
    advance_time(bodies)

print("part 1: " + str(find_energy(bodies)))

bodies = parse_input("./input/day12.txt")
axes = ['x', 'y', 'z']
steps = [-1, -1, -1]
step_ct = 0

while not found_all_steps(steps):
    advance_time(bodies)
    step_ct += 1
    for index, axis in enumerate(axes):
        if steps[index] < 0 and is_same_state(bodies, axis):
            steps[index] = step_ct

print("part 2: " + str(lcm.reduce(steps)))
