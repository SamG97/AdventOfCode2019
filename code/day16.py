import math

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
    signal = [int(c) for c in in_num]
    for _ in range(num_steps):
        signal = apply_phase(signal)
    return "".join([str(d) for d in signal])[:8]


def calculate_offset_fft(in_num, num_steps):
    offset = int(in_num[:7])
    in_length = len(in_num)
    full_length = in_length * 10000
    assert offset > full_length / 2, "Only works when offset in second half"
    digits_to_calc = full_length - offset
    num_copies = math.ceil(digits_to_calc / in_length)
    signal = [int(c) for c in in_num] * num_copies
    signal = signal[-digits_to_calc:]

    for _ in range(num_steps):
        out_val = 0
        for idx in range(digits_to_calc - 1, -1, -1):
            out_val += signal[idx]
            signal[idx] = abs(out_val) % 10
    return "".join([str(d) for d in signal])[:8]


if __name__ == "__main__":
    with open("../input/day16.txt") as f:
        num = f.readline().strip("\n")
    print(calculate_offset_fft(num, 100))
