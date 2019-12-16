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


def searchChildNodes(target, node):
    if node.id == target:
        return node
    if not node.children:
        return None
    for child in node.children:
        found = searchChildNodes(target, child)
        if found:
            return found


def countNodeDepth(target, node):
    if node.id == target:
        return 0
    # This is so inefficient.
    for child in node.children:
        if searchChildNodes(target, child):
            return countNodeDepth(target, child) + 1


def countOrbits(head, depth):
    if not head.children:
        return depth
    subtotal = depth
    for child in head.children:
        subtotal += countOrbits(child, depth + 1)
    return subtotal


def buildOrbitTree(orbits):
    # Prime loop with inital COM node
    cur = OrbitNode("COM", None, None)
    head = cur
    for orbit in orbits:
        # This will bubble the pointer back up to the node's common ancestor
        while cur and cur.id != orbit.orbitee:
            # Search new cur's children
            curtemp = searchChildNodes(orbit.orbitee, cur.parent)
            if curtemp:
                cur = curtemp
            else:
                cur = cur.parent
        lead = OrbitNode(orbit.orbiter, cur, None)
        cur.children.append(lead)
        cur = lead
    return head


def findDistance(src, dest):
    distance = 0
    cur = src.parent
    while cur.id != dest.parent:
        curtemp = searchChildNodes(dest.id, cur)
        if curtemp:
            return distance + countNodeDepth(dest.id, cur) - 1
        cur = cur.parent
        distance += 1


orbits = prep_input("./input/day6.txt")
sortOrbits(orbits)
head = buildOrbitTree(orbits)
santa = searchChildNodes("SAN", head)
you = searchChildNodes("YOU", head)

print("part 1: " + str(countOrbits(head, 0)))
print("part 2: " + str(findDistance(santa, you)))
