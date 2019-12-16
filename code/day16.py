base_pattern = [0, 1, 0, -1]


def get_multiplier(in_pos, out_pos):
    return base_pattern[((in_pos + 1) // out_pos) % 4]


def apply_phase(in_signal):
    out_signal = [0] * len(in_signal)
    for i in range(len(in_signal)):
        out_val = 0
        for j in range(len(in_signal)):
            out_val += in_signal[j] * get_multiplier(j, i + 1)
        out_signal[i] = abs(out_val) % 10
    return out_signal


def calculate_fft(in_num, num_steps):
    signal = [int(c) for c in str(in_num)]
    for _ in range(num_steps):
        signal = apply_phase(signal)
    return "".join([str(d) for d in signal])[:8]


if __name__ == "__main__":
    with open("../input/day16.txt") as f:
        num = int(f.readline())
    print(calculate_fft(num, 100))
