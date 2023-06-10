import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple

Improvement = namedtuple("Improvement", ["change", "args", "function"])


def calculate_path_length(matrix: np.ndarray, path: np.ndarray) -> float:
    length = matrix[path[0], path[-1]]
    for i in range(0, len(path)-1):
        length += matrix[path[i], path[i+1]]
    return length


def calculate_cycle_length(matrix: np.ndarray, cycle: np.ndarray) -> float:
    length = 0
    for i in range(0, len(cycle)-1):
        length += matrix[cycle[i], cycle[i+1]]
    return length


def draw_cycles(cycles, vertices):
    colors = ["red", "blue"]

    pairs_a = [vertices[i] for i in cycles[0]]
    pairs_b = [vertices[i] for i in cycles[1]]

    plt.figure(figsize=(12, 8), facecolor='white')
    plt.scatter(vertices[:, 0], vertices[:, 1], c="black")
    
    for i, cycle in enumerate([pairs_a, pairs_b]):
        for start, end in zip(cycle, cycle[1:]):
            plt.plot((start[0], end[0]), (start[1], end[1]), c=colors[i])
    plt.show()
