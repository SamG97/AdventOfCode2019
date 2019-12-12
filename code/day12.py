import numpy as np


class Moon:
    def __init__(self, starting_pos):
        self.pos = starting_pos
        self.velocity = np.zeros(3, dtype=np.int32)

    def move(self):
        self.pos += self.velocity

    def apply_gravity(self, other):
        less = self.pos < other.pos
        more = self.pos > other.pos
        self.velocity[less] += 1
        self.velocity[more] -= 1

    def __str__(self):
        return (
            f"pos=<x={self.pos[0]}, y={self.pos[1]}, z={self.pos[2]}>, "
            f"vel=<x={self.velocity[0]}, y={self.velocity[1]}, "
            f"z={self.velocity[2]}>"
        )


def step(moons):
    for moon in moons:
        for other_moon in moons:
            if moon == other_moon:
                continue
            moon.apply_gravity(other_moon)
    for moon in moons:
        moon.move()


def simulate(data, steps):
    moons = [
        Moon(np.array([int(c.strip("<> ")[2:])
        for c in l.split(",")])) for l in data
    ]
    for _ in range(steps):
        step(moons)
    return sum([
        np.sum(np.abs(moon.pos)) * np.sum(np.abs(moon.velocity))
        for moon in moons
    ])


def find_repeat(data):
    moons = [
        Moon(np.array([int(c.strip("<> ")[2:]) for c in l.split(",")]))
        for l in data
    ]
    xs = set()
    ys = set()
    zs = set()
    repeat = [None, None, None]
    step_count = 0
    while True:
        x_key = tuple((moon.pos[0], moon.velocity[0]) for moon in moons)
        y_key = tuple((moon.pos[1], moon.velocity[1]) for moon in moons)
        z_key = tuple((moon.pos[2], moon.velocity[2]) for moon in moons)
        if repeat[0] is None and x_key in xs:
            repeat[0] = step_count
        else:
            xs.add(x_key)
        if repeat[1] is None and y_key in ys:
            repeat[1] = step_count
        else:
            ys.add(y_key)
        if repeat[2] is None and z_key in zs:
            repeat[2] = step_count
        else:
            zs.add(z_key)
        if None not in repeat:
            break
        step(moons)
        step_count += 1
    return np.lcm.reduce(repeat)


if __name__ == "__main__":
    with open("../input/day12.txt") as f:
        d = [l.strip("\n") for l in f]
    print(find_repeat(d))
