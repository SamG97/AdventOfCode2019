import sys


def plot_wire(wire):
    visited = set()
    step_count = dict()
    moves = wire.split(",")
    pos = (0, 0)
    count = 0
    for move in moves:
        direction = move[0]
        distance = int(move[1:])
        for _ in range(distance):
            if direction == "U":
                pos = (pos[0], pos[1] + 1)
            elif direction == "D":
                pos = (pos[0], pos[1] - 1)
            elif direction == "R":
                pos = (pos[0] + 1, pos[1])
            elif direction == "L":
                pos = (pos[0] - 1, pos[1])
            else:
                raise RuntimeError(f"Unknown direction {direction}")
            count += 1
            visited.add(pos)
            if not pos in step_count:
                step_count[pos] = count
    return visited, step_count


if __name__ == "__main__":
    collisions = None
    counts = []
    with open("../input/day3.txt") as f:
        for wire in f:
            visits, steps = plot_wire(wire.strip("\n"))
            counts.append(steps)
            if collisions:
                collisions = collisions.intersection(visits)
            else:
                collisions = visits
    
    min_dist = sys.maxsize
    for point in collisions:
        dist = 0
        for count in counts:
            dist += count[point]
        min_dist = min(dist, min_dist)
    print(min_dist)
