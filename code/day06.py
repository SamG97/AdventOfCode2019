class Planet:
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.children = []
        self.count = None

    def count_parents(self, count):
        self.count = count
        for child in self.children:
            child.count_parents(self.count + 1)


def create_orbits(data):
    planets = {"COM": Planet(None, "COM")}
    for line in data:
        parent_name, child_name = line.strip("\n").split(")")
        child = Planet(parent_name, child_name)
        planets[child_name] = child
    data.seek(0)
    for line in data:
        parent_name, child_name = line.strip("\n").split(")")
        planets[parent_name].children.append(planets[child_name])
    return planets


def find_path(planets):
    def search(target):
        to_search = [(planets["COM"], [])]
        while len(to_search) > 0:
            candidate, candidate_path = to_search.pop(0)
            if candidate.name == target:
                return candidate_path

            new_path = candidate_path[:]
            new_path.append(candidate.name)
            for child in candidate.children:
                to_search.append((child, new_path))
        return None

    you_path = search("YOU")
    santa_path = search("SAN")
    same = 0
    for same in range(min(len(you_path), len(santa_path))):
        if you_path[same] != santa_path[same]:
            break
    return len(you_path) + len(santa_path) - (2 * same)


if __name__ == "__main__":
    with open("../input/day06.txt") as f:
        p = create_orbits(f)
    print(find_path(p))
