import numpy as np
from collections import defaultdict


def find_teleports(grid):
    rows, cols = grid.shape
    teleports = defaultdict(lambda: [])
    outers = set()
    start = None
    end = None
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] not in ["#", "."]:
                if grid[i + 1, j] not in ["#", "."]:
                    key = grid[i, j] + grid[i + 1, j]
                    if i < rows - 2 and grid[i + 2, j] == ".":
                        pos = (i + 2, j)
                    else:
                        pos = (i - 1, j)
                    grid[i + 1, j] = "#"
                    is_outer = i == 0 or i == rows - 2
                else:
                    key = grid[i, j] + grid[i, j + 1]
                    if j < cols - 2 and grid[i, j + 2] == ".":
                        pos = (i, j + 2)
                    else:
                        pos = (i, j - 1)
                    grid[i, j + 1] = "#"
                    is_outer = j == 0 or j == cols - 2
                if key == "AA":
                    start = pos
                elif key == "ZZ":
                    end = pos
                else:
                    teleports[key].append(pos)
                if is_outer:
                    outers.add(pos)
                grid[i, j] = "#"

    assert np.sum((grid != "#") & (grid != ".")) == 0, "Missed teleports"
    pairs = {}
    for _, (left, right) in teleports.items():
        pairs[left] = right
        pairs[right] = left
    return pairs, outers, start, end


def search(grid, teleports, outers, start, end):
    frontier = [(start, 0, 0)]
    visited = set()
    while len(frontier) > 0:
        pos, level, steps = frontier.pop(0)
        if (pos, level) in visited:
            continue
        if pos == end and level == 0:
            return steps
        visited.add((pos, level))

        for x, y in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            new_pos = (pos[0] + x, pos[1] + y)
            if grid[new_pos[0], new_pos[1]] == "." and new_pos not in visited:
                frontier.append((new_pos, level, steps + 1))
        
        if pos in teleports.keys():
            is_outer = pos in outers
            if is_outer and level == 0:
                continue
            level_change = -1 if is_outer else 1
            frontier.append((teleports[pos], level + level_change, steps + 1))
    return -1


if __name__ == "__main__":
    with open("../input/day20.txt") as f:
        g = np.array([[c for c in l.strip("\n")] for l in f])
    g[g == " "] = "#"
    t, o, s, e = find_teleports(g)
    print(search(g, t, o, s, e))
