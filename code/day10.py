import math

from collections import defaultdict

def count_observable(grid, station):
    station_x, station_y = station
    angles = set()
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (x, y) == station or grid[y][x] == ".":
                continue
            diff_x = x - station_x
            diff_y = y - station_y
            factor = math.gcd(abs(diff_x), abs(diff_y))
            diff_x /= factor
            diff_y /= factor
            angles.add((diff_x, diff_y))
    return len(angles)


def find_max_observable(grid):
    max_count = 0
    best_pos = None
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "#":
                count = count_observable(grid, (x, y))
                if count > max_count:
                    max_count = count
                    best_pos = (x, y)
    return max_count, best_pos


def find_200th_to_vaporize(grid, station):
    station_x, station_y = station
    asteroids = defaultdict(lambda: [])
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (x, y) == station or grid[y][x] == ".":
                continue
            diff_x = x - station_x
            diff_y = y - station_y
            factor = math.gcd(abs(diff_x), abs(diff_y))
            diff_x /= factor
            diff_y /= factor
            asteroids[(diff_x, diff_y)].append((x, y))
    angles = list(asteroids.keys())
    cycle_fraction = 200 % len(angles)
    full_cycles = 200 // len(angles)
    angles.sort(key=lambda pos: (math.atan2(pos[1], pos[0]) + (math.pi / 2)) % (math.pi * 2))
    candidates = asteroids[angles[cycle_fraction - 1]]
    candidates.sort(key=lambda pos: abs(pos[0] - station_x) + abs(pos[1]) - station_y)
    return candidates[full_cycles]


if __name__ == "__main__":
    with open("../input/day10.txt") as f:
        grid = [[c for c in l.strip("\n")] for l in f]
    s = find_max_observable(grid)[1]
    pos = find_200th_to_vaporize(grid, s)
    print(pos[0] * 100 + pos[1])
