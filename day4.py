def has_adjacent_digits(number):
    cur_digit = number % 10
    number = number // 10
    while number > 0:
        last_digit = cur_digit
        cur_digit = number % 10
        if last_digit == cur_digit:
            return True
        number = number // 10
    return False


def has_strict_double(number):
    cur_digit = number % 10
    number = number // 10
    trail_digit = -1
    while number > 0:
        last_digit = cur_digit
        cur_digit = number % 10
        # if there is a next digit, check that it and the trailing digit
        # aren't the same as cur_digit.
        if last_digit == cur_digit and number > 9:
            future_digit = ((number // 10) % 10)
            if cur_digit != future_digit and cur_digit != trail_digit:
                return True
        # if this is the last digit, check the trailing digit against cur_digit
        elif last_digit == cur_digit and trail_digit != cur_digit:
            return True
        number = number // 10
        trail_digit = last_digit
    return False


def is_decreasing(number):
    cur_digit = number % 10
    number = number // 10
    while number > 0:
        last_digit = cur_digit
        cur_digit = number % 10
        if cur_digit > last_digit:
            return False
        number = number // 10
    return True


lower_bound = 254032
upper_bound = 789860
num_candidates_p1 = 0
num_candidates_p2 = 0

for i in range(lower_bound, upper_bound):
    if has_adjacent_digits(i) and is_decreasing(i):
        num_candidates_p1 += 1
    if has_strict_double(i) and is_decreasing(i):    
        num_candidates_p2 += 1

print("part 1: %d" % num_candidates_p1)
print("part 2: %d" % num_candidates_p2)
