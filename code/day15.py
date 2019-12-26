import numpy as np
from collections import defaultdict

from day11 import execute

directions = {
    1: np.array([0, 1]),
    2: np.array([0, -1]),
    3: np.array([-1, 0]),
    4: np.array([1, 0]),
}


def create_map(program):
    def add_candidates(l, pos, state, c, r, cnt):
        for cmd, move in directions.items():
            l.append((pos + move, cmd, state[:], c, r, cnt + 1))

    explored_nodes = defaultdict(lambda: -1)
    oxygen_location = None
    oxygen_steps = None
    explored_nodes[(0, 0)] = 1
    frontier = []
    add_candidates(frontier, np.array([0, 0]), program, 0, 0, 0)
    while len(frontier) > 0:
        new_pos, instr, s, pc, rb, steps = frontier.pop(0)
        if explored_nodes[tuple(new_pos)] != -1:
            continue
        out, pc, rb = execute(s, [instr], pc, rb)
        explored_nodes[tuple(new_pos)] = out
        if out == 2:
            oxygen_location = new_pos
            oxygen_steps = steps
        if out != 0:
            add_candidates(frontier, new_pos, s, pc, rb, steps)
    return oxygen_location, oxygen_steps, explored_nodes


def fill_oxygen(locations, oxygen_location):
    frontier = [np.array(oxygen_location)]
    steps = 0
    while 1 in locations.values():
        steps += 1
        new_frontier = []
        for loc in frontier:
            for move in directions.values():
                new_pos = loc + move
                if locations[tuple(new_pos)] != 1:
                    continue
                locations[tuple(new_pos)] = 2
                new_frontier.append(new_pos)
        frontier = new_frontier
    return steps


if __name__ == "__main__":
    with open("../input/day15.txt") as f:
        program_text = f.readline()
    p = [int(val) for val in program_text.split(",")]
    o_loc, o_steps, nodes = create_map(p)
    print(o_steps)
    print(fill_oxygen(nodes, o_loc))
