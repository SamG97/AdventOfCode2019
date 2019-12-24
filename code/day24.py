from collections import defaultdict


class GameOfLife:
    def __init__(self, grid):
        if type(grid) == GameOfLife:
            self.board = grid.board
            self.num_rows = grid.num_rows
            self.num_cols = grid.num_cols
        else:
            acc = 0
            factor = 1
            for row in grid:
                for col in row:
                    acc += col * factor
                    factor *= 2
            self.board = acc
            self.num_rows = len(grid)
            self.num_cols = len(grid[0])

    def get_cell(self, row, col):
        if row < 0 or row >= self.num_rows:
            return 0
        if col < 0 or col >= self.num_cols:
            return 0
        idx = row * self.num_cols + col
        return self.board >> idx & 0b1

    def set_cell(self, row, col, val):
        idx = row * self.num_cols + col
        if val:
            self.board = self.board | (0b1 << idx)
        else:
            self.board = self.board & ~(0b1 << idx)

    def update_board(self):
        new_board = GameOfLife(self)
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                alive_count = 0
                for neighbour in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    alive_count += self.get_cell(
                        row + neighbour[0], col + neighbour[1])
                if self.get_cell(row, col):
                    if alive_count != 1:
                        new_board.set_cell(row, col, 0)
                elif 1 <= alive_count <= 2:
                    new_board.set_cell(row, col, 1)
        return new_board

    def print_board(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.get_cell(row, col):
                    print("#", end="")
                else:
                    print(".", end="")
            print()


class RecursiveGameOfLife:
    def __init__(self, grid):
        if type(grid) == RecursiveGameOfLife:
            self.boards = grid.boards.copy()
            self.num_rows = grid.num_rows
            self.num_cols = grid.num_cols
        else:
            acc = 0
            factor = 1
            for row in grid:
                for col in row:
                    acc += col * factor
                    factor *= 2
            self.boards = defaultdict(lambda: 0)
            self.boards[0] = acc
            self.num_rows = len(grid)
            self.num_cols = len(grid[0])
            assert (
                self.num_rows % 2 and self.num_cols % 2
            ), "Must have a grid with odd dimensions"

    def get_cell(self, layer, row, col, move=None):
        row_mid = self.num_rows // 2
        col_mid = self.num_cols // 2
        if row < 0:
            return self.get_cell(layer - 1, row_mid - 1, 2)
        elif row >= self.num_rows:
            return self.get_cell(layer - 1, row_mid + 1, 2)
        elif col < 0:
            return self.get_cell(layer - 1, 2, col_mid - 1)
        elif col >= self.num_cols:
            return self.get_cell(layer - 1, 2, col_mid + 1)
        elif row == row_mid and col == col_mid:
            acc = 0
            if move == (-1, 0):
                for c in range(5):
                    acc += self.get_cell(layer + 1, self.num_rows - 1, c)
            elif move == (1, 0):
                for c in range(5):
                    acc += self.get_cell(layer + 1, 0, c)
            elif move == (0, -1):
                for r in range(5):
                    acc += self.get_cell(layer + 1, r, self.num_cols - 1)
            elif move == (0, 1):
                for r in range(5):
                    acc += self.get_cell(layer + 1, r, 0)
            else:
                raise RuntimeError(
                    f"Must provide direction of travel when moving into"
                    f"centre cell"
                )
            return acc
        idx = row * self.num_cols + col
        return self.boards[layer] >> idx & 0b1

    def set_cell(self, layer, row, col, val):
        idx = row * self.num_cols + col
        if val:
            new_board = self.boards[layer] | (0b1 << idx)
        else:
            new_board = self.boards[layer] & ~(0b1 << idx)
        self.boards[layer] = new_board

    def update_board(self):
        new_board = RecursiveGameOfLife(self)
        current_layers = list(self.boards.keys())
        min_layer = min(current_layers)
        max_layer = max(current_layers)
        row_mid = self.num_rows // 2
        col_mid = self.num_cols // 2
        for layer in current_layers + [min_layer - 1, max_layer + 1]:
            for row in range(self.num_rows):
                for col in range(self.num_cols):
                    if row == row_mid and col == col_mid:
                        continue
                    alive_count = 0
                    for neighbour in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                        alive_count += self.get_cell(
                            layer, row + neighbour[0], col + neighbour[1],
                            neighbour
                        )
                    if self.get_cell(layer, row, col):
                        if alive_count != 1:
                            new_board.set_cell(layer, row, col, 0)
                    elif 1 <= alive_count <= 2:
                        new_board.set_cell(layer, row, col, 1)
        return new_board

    def count_bugs(self):
        row_mid = self.num_rows // 2
        col_mid = self.num_cols // 2
        count = 0
        for layer in self.boards.keys():
            for row in range(self.num_rows):
                for col in range(self.num_cols):
                    if row == row_mid and col == col_mid:
                        continue
                    count += self.get_cell(layer, row, col)
        return count

    def print_board(self):
        row_mid = self.num_rows // 2
        col_mid = self.num_cols // 2
        for layer in self.boards.keys():
            print(f"Depth {layer}")
            for row in range(self.num_rows):
                for col in range(self.num_cols):
                    if row == row_mid and col == col_mid:
                        print("?", end="")
                    elif self.get_cell(layer, row, col):
                        print("#", end="")
                    else:
                        print(".", end="")
                print()


if __name__ == "__main__":
    with open("../input/day24.txt") as f:
        grid = [[1 if c == "#" else 0 for c in l.strip("\n")] for l in f]

    # Part 1
    game = GameOfLife(grid)
    seen = set()
    seen.add(game.board)
    while True:
        game = game.update_board()
        score = game.board
        if score in seen:
            break
        else:
            seen.add(score)
    print(f"First score seen twice: {score}")

    # Part 2
    game = RecursiveGameOfLife(grid)
    for _ in range(200):
        game = game.update_board()
    print(f"Recursive count after 200 mins: {game.count_bugs()}")
