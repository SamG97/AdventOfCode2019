import numpy as np

from day11 import execute


def calc_blocks(program):
    val = pc = rb = 0
    screen = np.zeros((38, 22), dtype=np.int8)
    output = []
    while val != "HALT":
        val, pc, rb = execute(program, [], pc, rb)
        output.append(val)
        if len(output) == 3:
            screen[output[0], output[1]] = output[2]
            output = []
    return np.sum(screen == 2)


def play_game(program):
    val = pc = rb = 0
    screen = np.zeros((38, 22), dtype=np.int8)
    output = []
    last_score = 0
    while val != "HALT":
        ball_pos = np.argwhere(screen == 4)
        paddle_pos = np.argwhere(screen == 3)
        if ball_pos.shape[0] == 0 or paddle_pos.shape[0] == 0:
            direction = 0
        else:
            ball_x = ball_pos[0][0]
            paddle_x = paddle_pos[0][0]
            if ball_x == paddle_x:
                direction = 0
            elif ball_x < paddle_x:
                direction = -1
            else:
                direction = 1
        val, pc, rb = execute(program, [direction], pc, rb)
        output.append(val)
        if len(output) == 3:
            if output[0] == -1 and output[1] == 0:
                last_score = output[2]
            screen[output[0], output[1]] = output[2]
            output = []
    print(last_score)


if __name__ == "__main__":
    with open("../input/day13.txt") as f:
        program_text = f.readline()
    p = [int(val) for val in program_text.split(",")]
    p[0] = 2
    play_game(p)
