import numpy as np
from collections import defaultdict


def find_teleports(grid):
    rows, cols = grid.shape
    teleports = defaultdict(lambda: [])
    start = None
    end = None
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] not in ["#", "."]:
                if grid[i + 1, j] not in ["#", "."]:
                    key = grid[i, j] + grid[i + 1, j]
                    if i == 0:
                        pos = (i + 2, j)
                    else:
                        pos = (i - 1, j)
                    grid[i + 1, j] = "#"
                else:
                    key = grid[i, j] + grid[i, j + 1]
                    if j == 0:
                        pos = (i, j + 2)
                    else:
                        pos = (i, j - 1)
                    grid[i, j + 1] = "#"
                if key == "AA":
                    start = pos
                elif key == "ZZ":
                    end = pos
                else:
                    teleports[key].append(pos)
                grid[i, j] = "#"

    assert np.sum((grid != "#") & (grid != ".")) == 0
    return teleports, start, end


if __name__ == "__main__":
    with open("../input/day20.txt") as f:
        g = np.array([[c for c in l.strip("\n")] for l in f])
    g[g == " "] = "#"
    t = find_teleports(g)
    print(t)
