class OrbitPair:
    def __init__(self, orbitee, orbiter):
        self.orbitee = orbitee
        self.orbiter = orbiter


class OrbitNode:
    def __init__(self, id, parent, child):
        self.id = id
        self.parent = parent
        self.children = []
        if child is not None:
            self.children.append(child)


def prep_input(path):
    with open(path) as f:
        orbits_raw = f.readlines()
    orbits = []
    for orbit in orbits_raw:
        pair = orbit.rstrip().split(")")
        pair = OrbitPair(pair[0], pair[1])
        orbits.append(pair)
    return orbits


def sortOrbits(orbits):
    if len(orbits) <= 1:
        return

    # Put "COM" first
    for i in range(0, len(orbits)):
        if orbits[i].orbitee == "COM":
            temp = orbits[0]
            orbits[0] = orbits[i]
            orbits[i] = temp

    # Sort the rest of the orbit pairs
    trail, inner, lead = (1, 1, 1)
    target = orbits[0].orbiter
    while trail < len(orbits):
        while lead < len(orbits):
            if orbits[lead].orbitee == target:
                temp = orbits[inner]
                orbits[inner] = orbits[lead]
                orbits[lead] = temp
                inner += 1
            lead += 1
        target = orbits[trail].orbiter
        trail += 1
        lead = inner
    return


def countOrbits(orbits, planet, index):
    if index == 0:
        return 1
    # Find index of next time planet appears
    while orbits[index].orbiter != planet:
        index -= 1
    return countOrbits(orbits, orbits[index].orbitee, index) + 1


def countTotalOrbits(orbits):
    if len(orbits) <= 1:
        return 1
    numOrbits = 0
    index = len(orbits) - 1
    for orbit in reversed(orbits):
        numOrbits += countOrbits(orbits, orbit.orbitee, index)
        index -= 1
    return numOrbits


orbits = prep_input("./input/day6.txt")
sortOrbits(orbits)

print("part 1: " + str(countTotalOrbits(orbits)))
