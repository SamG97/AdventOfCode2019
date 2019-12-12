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
            f"vel=<x={self.velocity[0]}, y={self.velocity[1]}, z={self.velocity[2]}>"
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
    moons = [Moon(np.array([int(c.strip("<> ")[2:]) for c in l.split(",")])) for l in data]
    for s in range(steps):
        step(moons)
        if s % 100000 == 0:
            print(s)
    return sum([np.sum(np.abs(moon.pos)) * np.sum(np.abs(moon.velocity)) for moon in moons])


if __name__ == "__main__":
    with open("../input/day12.txt") as f:
        d = [l.strip("\n") for l in f]
    print(simulate(d, 4686774924))
