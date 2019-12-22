import sympy
import numpy as np


def new_stack(deck):
    return list(reversed(deck))


def cut(n, deck):
    return deck[n:] + deck[:n]


def increment(n, deck):
    cards = len(deck)
    new_deck = [None] * cards
    for i, card in enumerate(deck):
        new_deck[(i * n) % cards] = card
    return new_deck


def shuffle(instructions, deck):
    for instruction in instructions:
        instruction = instruction.strip("\n")
        if instruction == "deal into new stack":
            deck = new_stack(deck)
        elif "cut" in instruction:
            instruction = instruction.replace("cut ", "")
            deck = cut(int(instruction), deck)
        elif "increment" in instruction:
            instruction = instruction.replace("deal with increment ", "")
            deck = increment(int(instruction), deck)
        else:
            raise RuntimeError(f"Unknown instruction: {instruction}")
    return deck


def modular_matmul(a, b, base):
    n, m = a.shape
    assert a.shape == b.shape
    c = np.zeros_like(a, dtype=np.int64)
    for i in range(n):
        for j in range(m):
            total = 0
            for k in range(n):
                # Cast to arbitrary precision since we need >64 bits to
                # represent even a single multiplication
                total = (total + int(a[i, k]) * int(b[k, j]))
            c[i, j] = total % base
    return c


def modular_pow(base, exponent, modulus):
    if modulus == 1:
        return np.zeros_like(base)
    result = np.zeros_like(base)
    np.fill_diagonal(result, 1)
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            # Computation overflows int64 which is the largest dtype in numpy
            # so have to implement matmul ourselves
            result = modular_matmul(result, base, modulus)
        exponent = exponent >> 1
        base = modular_matmul(base, base, modulus)
    return result


def shuffle_index(instructions, cards, repeats, idx):
    a = 1
    b = 0
    for instruction in instructions:
        instruction = instruction.strip("\n")
        if instruction == "deal into new stack":
            a *= -1
            b = -b - 1
        elif "cut" in instruction:
            instruction = instruction.replace("cut ", "")
            b -= int(instruction)
        elif "increment" in instruction:
            instruction = instruction.replace("deal with increment ", "")
            fact = int(instruction)
            a *= fact
            b *= fact
        else:
            raise RuntimeError(f"Unknown instruction: {instruction}")
    a = a % cards
    b = b % cards

    inv_a, _, g = sympy.numbers.igcdex(a, cards)
    assert g == 1, f"{a} has no modular inverse base {cards}"
    inv_a = inv_a % cards
    inv_b = (-b * inv_a) % cards
    op = np.array([[inv_a, inv_b], [0, 1]], dtype=np.int64)
    op = modular_pow(op, repeats, cards)
    # [f^n(x) 1] = [[a b][0 1]]^n [x 1]
    return np.matmul(op, [idx, 1])[0] % cards


if __name__ == "__main__":
    with open("../input/day22.txt") as f:
        instrs = f.readlines()
    print(shuffle_index(instrs, 119315717514047, 101741582076661, 2020))
