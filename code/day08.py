from collections import defaultdict
import numpy as np
from matplotlib import pyplot as plt


def count_layers(image, width, height):
    num_layers = len(image) / (width * height)
    assert num_layers % 1 == 0
    num_layers = int(num_layers)
    offset = 0
    counts = []
    for _ in range(num_layers):
        count = defaultdict(lambda: 0)
        for _ in range(width * height):
            val = int(image[offset])
            count[val] += 1
            offset += 1
        counts.append(count)
    assert offset == len(image)

    min_zeros = float("inf")
    min_layer = -1
    for i, layer in enumerate(counts):
        layer_zeros = layer[0]
        if layer_zeros < min_zeros:
            min_zeros = layer_zeros
            min_layer = i
    return counts[min_layer][1] * counts[min_layer][2]


def render_image(image, width, height):
    num_layers = len(image) / (width * height)
    assert num_layers % 1 == 0
    num_layers = int(num_layers)
    final_image = [2] * (width * height)
    for layer in range(num_layers):
        offset = layer * width * height
        for i in range(width * height):
            if final_image[i] == 2:
                final_image[i] = int(image[offset + i])

    return final_image


def print_image(image, width, height):
    data = np.zeros((height, width, 3), dtype=np.uint8)
    for h in range(height):
        for w in range(width):
            index = h * width + w
            if image[index] == 1:
                data[h, w] = [255] * 3
    plt.imshow(data, interpolation='nearest')
    plt.show()


if __name__ == "__main__":
    with open("../input/day08.txt") as f:
        print_image(render_image(f.readline().strip("\n"), 25, 6), 25, 6)
