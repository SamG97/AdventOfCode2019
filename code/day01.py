import numpy as np


def calc_fuel(weight):
    return max(0, int(np.floor(weight / 3) - 2))


def calc_fuel_adv(weight):
    rec_calc = weight
    fuel_sum = 0
    while True:
        val = calc_fuel(rec_calc)
        if val == 0:
            return fuel_sum
        else:
            fuel_sum += val
            rec_calc = val


if __name__ == "__main__":
    with open("../input/day01.txt") as f:
        print(sum([calc_fuel_adv(int(line)) for line in f]))
