import random
import numpy as np
from helpers import draw_cycles 

def extend_cycle(cycle: np.ndarray, matrix: np.ndarray, free_vertices: np.ndarray):
    random_index = np.random.choice(np.where(free_vertices == 1)[0])
    free_vertices[random_index] = 0

    return np.append(cycle, random_index)

def random_generator(matrix: np.ndarray, vertices: np.ndarray, start_ver: int = None, draw: bool = False):
    if start_ver is None:
        start_ver_a = random.randint(0, 99)
    else:
        start_ver_a = start_ver
    start_ver_b = np.argmax(matrix[:, start_ver_a])

    free_vertices = np.ones(100)
    free_vertices[start_ver_a] = 0
    free_vertices[start_ver_b] = 0

    cycle_a = np.array([start_ver_a])
    cycle_b = np.array([start_ver_b])

    while sum(free_vertices) > 0:
        cycle_a = extend_cycle(cycle_a, matrix, free_vertices)
        cycle_b = extend_cycle(cycle_b, matrix, free_vertices)

    if draw:
        draw_cycles((cycle_a, cycle_b), vertices)

    cycle_a = np.append(cycle_a, cycle_a[0])
    cycle_b = np.append(cycle_b, cycle_b[0])

    return cycle_a, cycle_b