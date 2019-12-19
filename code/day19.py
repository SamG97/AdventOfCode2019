from day11 import execute


def count_pulls(program):
    count = 0
    left = right = 0
    for y in range(50):
        left_val = 0
        while not left_val:
            left_val, _, _ = execute(program[:], [left, y])
            if not left_val:
                left += 1
        right_val = 1
        if y < 5:
            # Special case deals with 1 width beam moving >1 space between rows
            seen_beam = False
            for x in range(10):
                right_val, _, _ = execute(program[:], [x, y])
                if right_val:
                    seen_beam = True
                elif seen_beam:
                    break
            right = x
        else:
            while right_val:
                right_val, _, _ = execute(program[:], [right, y])
                if right_val:
                    right += 1
        row_len = min(right, 50) - min(left, 50)
        count += row_len
    return count


def find_box(program, box_size):
    left = right = 0
    ends = []
    y = 0
    while True:
        left_val = 0
        while not left_val:
            left_val, _, _ = execute(program[:], [left, y])
            if not left_val:
                left += 1
        right_val = 1
        if y < 5:
            # Special case deals with 1 width beam moving >1 space between rows
            seen_beam = False
            for x in range(10):
                right_val, _, _ = execute(program[:], [x, y])
                if right_val:
                    seen_beam = True
                elif seen_beam:
                    break
            right = x
        else:
            while right_val:
                right_val, _, _ = execute(program[:], [right, y])
                if right_val:
                    right += 1
        ends.append(right)
        if (
            right - left >= box_size and \
                ends[y + 1 - box_size] > left + box_size - 1
        ):
            return left * 10000 + y + 1 - box_size
        y += 1


if __name__ == "__main__":
    with open("../input/day19.txt") as f:
        program_text = f.readline()
    program = [int(val) for val in program_text.split(",")]
    print(count_pulls(program))
    print(find_box(program, 100))
