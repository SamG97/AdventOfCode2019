import heapq
import numpy as np
from collections import defaultdict


def import_grid(data):
    grid = [[c for c in l.strip("\n")] for l in data]
    return np.array(grid).transpose((1, 0))


moves = (
    np.array([0, 1]), np.array([0, -1]), np.array([-1, 0]), np.array([1, 0])
)


def find_shortest_paths(grid, root, robot_symbols):
    empty_cells = robot_symbols + (".",)

    def get_val(arr, idxs):
        return arr[idxs[0], idxs[1]]

    paths = {}
    pos = np.argwhere(grid == root)[0]
    visited = np.zeros_like(grid, np.bool)
    visited[pos[0], pos[1]] = 1
    frontier = [(pos, 0, set())]
    while len(frontier) > 0:
        pos, steps, doors = frontier.pop(0)
        for move in moves:
            new_pos = pos + move
            contents = get_val(grid, new_pos)
            if contents == "#" or get_val(visited, new_pos):
                continue
            visited[new_pos[0], new_pos[1]] = 1
            if contents in empty_cells:
                frontier.append((new_pos, steps + 1, doors))
            elif 65 <= ord(contents) <= 90:  # Door
                new_doors = doors.copy()
                new_doors.add(contents)
                frontier.append(
                    (new_pos, steps + 1, new_doors)
                )
            else:  # Key
                assert 97 <= ord(contents) <= 122
                paths[contents] = (steps + 1, "".join(sorted(list(doors))))
                frontier.append((new_pos, steps + 1, doors))
    return paths


def find_all_paths(grid, robot_symbols):
    all_paths = {}
    for root in robot_symbols + tuple(chr(s) for s in range(97, 123)):
        # Assumes keys are always present in an order starting from 'a'
        if root not in grid:
            break
        all_paths[root] = find_shortest_paths(grid, root, robot_symbols)
    return all_paths


def a_star(paths, robot_symbols):
    num_robots = len(robot_symbols)
    num_keys_to_find = len(paths) - num_robots
    min_dist = np.inf
    for path in paths.values():
        values = [v[0] for v in path.values()]
        if len(values) > 0:
            min_dist = min(min_dist, min(values))

    def h(obtained_keys):
        # Multiplication by min_dist is safe since h is still admissible but
        # also larger than if just using the difference normally so we're more
        # likely to move forward with getting more keys on a good route than
        # spend all the time exploring every route of a certain depth
        return min_dist * (num_keys_to_find - len(obtained_keys))

    def can_move(obtained_keys, required_keys):
        for key in required_keys:
            if key not in obtained_keys:
                return False
        return True

    start_state = (robot_symbols, "")
    g_score = defaultdict(lambda: np.inf)
    g_score[start_state] = 0
    open_set = [(h(""), start_state)]
    visited_set = set()
    while len(open_set) > 0:
        score, (cur_syms, keys) = heapq.heappop(open_set)
        if (cur_syms, keys) in visited_set:
            continue  # Already visited

        if len(keys) == num_keys_to_find:
            return score

        for robot in range(num_robots):
            cur_sym = cur_syms[robot]
            for move, (dist, keys_needed) in paths[cur_sym].items():
                if move.upper() in keys:
                    continue  # Already visited key

                if not can_move(keys, keys_needed):
                    continue  # Don't own the keys we need to move

                tentative_g_score = g_score[(cur_syms, keys)] + dist
                new_keys = "".join(sorted(list(keys + move.upper())))
                new_pos = tuple(
                    cur_syms[:robot] + (move,) + cur_syms[robot+1:]
                )
                new_state = (new_pos, new_keys)
                if tentative_g_score < g_score[new_state]:
                    g_score[new_state] = tentative_g_score
                    h_score = h(new_keys)
                    f_score = tentative_g_score + h_score
                    heapq.heappush(open_set, (f_score, new_state))


if __name__ == "__main__":
    robots = ("0", "1", "2", "3")
    with open("../input/day18.txt") as f:
        g = import_grid(f.readlines())
    p = find_all_paths(g, robots)
    print(a_star(p, robots))
