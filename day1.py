def prep_day_1(path):
    with open(path) as f:
        numbers = f.readlines()
    numbers = list(map(int, numbers))
    return numbers


def calc_fuel_requirement(mass):
    fuel = mass//3 - 2
    if fuel <= 0:
        fuel = 0
    return fuel


def calc_total_fuel(mass):
    total_fuel = calc_fuel_requirement(mass)
    next_fuel = total_fuel

    while next_fuel > 0:
        next_fuel = calc_fuel_requirement(next_fuel)
        total_fuel += next_fuel

    return total_fuel


fuel = 0
numbers = prep_day_1("input/day1.txt")

for num in numbers:
    fuel += calc_fuel_requirement(num)

print("part 1 total fuel: " + str(fuel))

fuel = 0

for num in numbers:
    fuel += calc_total_fuel(num)

print("part 2 total fuel: " + str(fuel))

