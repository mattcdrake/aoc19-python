from sys import maxsize


def prep_input(path):
    with open(path) as f:
        raw_in = f.readlines()
    layers = []
    for i in range(0, len(raw_in[0]), 150):
        layers.append(raw_in[0][i:i+150])
    return layers


def count_char(layer, char):
    count = 0
    for digit in layer:
        if digit == char:
            count += 1
    return count


def find_fewest_zeroes(layers):
    fewest_layer = 0
    least_zeroes_ct = maxsize
    for index, layer in enumerate(layers):
        zeroes = count_char(layer, "0")
        if zeroes < least_zeroes_ct:
            least_zeroes_ct = zeroes
            fewest_layer = index
    return fewest_layer


layers = prep_input("input/day8.txt")
fewest_zeroes_layer = find_fewest_zeroes(layers)
ones = count_char(layers[fewest_zeroes_layer], "1")
twos = count_char(layers[fewest_zeroes_layer], "2")

print("part 1: " + str(ones * twos))
