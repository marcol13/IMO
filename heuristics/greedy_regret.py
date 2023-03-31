import random
import numpy as np

from helpers import calculate_cycle_length, draw_cycles

def init_cycle(index: int, matrix: np.ndarray, free_vertices: np.ndarray):
    """
    Create cycle from given vertex and vertex closest to the given one.
    :param index: index of the initial vertex.
    :param matrix: matrix with lengths between vertices.
    :param free_vertices: list with vertices which are not in a cycle.
    :return: inital cycle.
    """
    row = matrix[:, index]
    min_len = np.inf
    best_vertex = None
    for vertex in range(len(row)):
        if free_vertices[vertex] == 1 and row[vertex] < min_len:
            min_len = row[vertex]
            best_vertex = vertex
    free_vertices[best_vertex] = 0
    cycle = np.array([index, best_vertex, index])
    return cycle

def distance_diff(matrix: np.ndarray, cycle: np.ndarray, index: int, checked_vertex: int):
    """
    Calculate cost of inserting the vertex into the cycle.
    :param matrix: matrix with lengths between vertices.
    :param cycle: list with the vertices in the cycle.
    :param index: index of cycle for checking inserting point.
    :param checked_vertex: potential new vertex in the cycle.
    :return: cost of inserting vertex into cycle.
    """
    prev = cycle[index - 1]
    next = cycle[index]
    return matrix[prev, checked_vertex] + matrix[checked_vertex, next] - matrix[prev, next]

def find_best_with_regret(cycle: np.ndarray, matrix: np.ndarray, free_vertices: np.ndarray, alpha: float):
    """
    Finds best vertex among free vertices regards to 2-regret value.
    :param cycle: list with the vertices in the cycle.
    :param matrix: matrix with lengths between vertices.
    :param free_vertices: list with vertices which are not in a cycle.
    :param alpha: weight ratio used for calculate regret.
    :return: best vertex for insertion to cycle.
    """
    vertices = [i for i in range(len(matrix)) if free_vertices[i] == 1]
    distances = []

    for free_vertex in vertices:
        distances.append([distance_diff(matrix, cycle, cycle_vertex, free_vertex) for cycle_vertex in range(1, len(cycle))])

    distances = np.array(distances)
    if distances.shape[1] == 1:
        best_vertex = vertices[np.argmin(distances)]
    else:
        distances.sort()
        regret = np.array(list(map(lambda x: x[1] - alpha * x[0], distances)))
        best_vertex = vertices[np.argmax(regret)]

    return best_vertex

def extend_cycle(cycle: np.ndarray, matrix: np.ndarray, free_vertices: np.ndarray, alpha: float):
    """
    Add vertex which increase size of the cycle by the smallest amount.
    :param cycle: list with the vertices in the cycle.
    :param matrix: matrix with lengths between vertices.
    :param free_vertices: list with vertices which are not in a cycle.
    :param alpha: weight ratio used for calculate regret.
    :return: extended cycle.
    """
    best_vertex = find_best_with_regret(cycle, matrix, free_vertices, alpha)
    best_insertion = np.argmin([distance_diff(matrix, cycle, cycle_vertex, best_vertex) for cycle_vertex in range(1, len(cycle))])

    free_vertices[best_vertex] = 0

    return np.concatenate([cycle[:best_insertion + 1], [best_vertex], cycle[best_insertion + 1:]])

def greedy_regret(matrix: np.ndarray, vertices: np.ndarray, start_ver: int = None, draw: bool = False, alpha: float = 1.8):
    """
    Find solution for double TSP using greedy 2-regret approach.
    :param matrix: matrix with lengths between vertices.
    :param vertices: array with the coordinates of vertices.
    :param start_ver: optional argument, if int is passed it will be used as index of the first vertex.
    :param draw: pass True if results should be drawn, False otherwise.
    :param alpha: weight ratio used for calculate regret.
    """
    if start_ver is None:
        start_ver_a = random.randint(0, 100)
    else:
        start_ver_a = start_ver
    start_ver_b = np.argmax(matrix[:, start_ver_a])

    free_vertices = [1] * 100
    free_vertices[start_ver_a] = 0
    free_vertices[start_ver_b] = 0

    cycle_a = init_cycle(start_ver_a, matrix, free_vertices)
    cycle_b = init_cycle(start_ver_b, matrix, free_vertices)

    while sum(free_vertices) > 0:
        cycle_a = extend_cycle(cycle_a, matrix, free_vertices, alpha)
        cycle_b = extend_cycle(cycle_b, matrix, free_vertices, alpha)

    length_a = calculate_cycle_length(matrix, cycle_a)
    length_b = calculate_cycle_length(matrix, cycle_b)    

    if draw:
        draw_cycles([cycle_a, cycle_b], vertices)

    return length_a + length_b