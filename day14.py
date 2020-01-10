class Chemical:
    def __init__(self, count, name):
        self.count = count
        self.name = name


class Reaction:
    def __init__(self, reagents, product):
        self.reagents = reagents
        self.product = product


class ReactionNode:
    def __init__(self, reaction, parent):
        self.reaction = reaction
        self.parent = parent
        self.children = []


# Returns index of a reaction given a rhs product
def find_reaction(reactions, rhs):
    for index, reaction in enumerate(reactions):
        if reaction.product.name == rhs:
            return index
    return -1


def build_graph(reactions, chemical, parent):
    reaction = reactions[find_reaction(reactions, chemical)]
    cur_node = ReactionNode(reaction, parent)
    if parent is not None:
        parent.children.append(cur_node)
    if cur_node.reaction.reagents[0].name == "ORE":
        return
    for reagent in reaction.reagents:
        build_graph(reactions, reagent.name, cur_node)
    if cur_node.reaction.product.name == "FUEL":
        return cur_node


def calculate_cost(costs, node):
    product_cost = costs[node.reaction.product.name]
    product_yield = node.reaction.product.count
    reaction_ct = product_cost // product_yield
    if product_cost % product_yield > 0:
        reaction_ct += 1
    costs[node.reaction.product.name] -= product_yield * reaction_ct

    for reagent in node.reaction.reagents:
        try:
            costs[reagent.name] += reagent.count * reaction_ct
        except:
            costs[reagent.name] = reagent.count * reaction_ct

    for child in node.children:
        calculate_cost(costs, child)


def parse_chems_inner(string, start, end):
    chems = string[start:end].split(",")
    chems = list(map(str.split, map(str.strip, chems)))
    output = []
    for chem in chems:
        count = int(chem[0])
        name = chem[1]
        output.append(Chemical(count, name))
    return output


def parse_chems(string, side):
    if side == "lhs":
        start = 0
        end = string.find("=>")
    else:
        start = string.find("=>") + 2
        end = len(string)
    return parse_chems_inner(string, start, end)


def prep_input(path):
    with open(path) as f:
        reactions = f.readlines()
    output = []
    for reaction in reactions:
        lhs = parse_chems(reaction, "lhs")
        rhs = parse_chems(reaction, "rhs")[0]
        output.append(Reaction(lhs, rhs))
    return output


reactions = prep_input("./input/day14.txt")
graph_root = build_graph(reactions, "FUEL", None)
costs = {"FUEL": 1}
calculate_cost(costs, graph_root)
min_ore = costs["ORE"]
print("part 1: " + str(min_ore))

low = 1
high = 1000000000000
found = False
while not found:
    mid = (low + high) // 2
    costs = {"FUEL": (low + high) // 2}
    calculate_cost(costs, graph_root)
    ore_diff = 1000000000000 - costs["ORE"]
    if ore_diff < min_ore and ore_diff > 0:
        found = True
    elif ore_diff > 0:
        low = mid
    else:
        high = mid
print("part 2: " + str(mid))
