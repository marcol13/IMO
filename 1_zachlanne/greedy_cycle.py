import random
import numpy as np

from helpers import draw_cycles, calculate_cycle_length


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


def find_the_best_vertex(start: int, end: int, matrix: np.ndarray, free_vertices: np.ndarray):
    """
    For the given points find vertex which connect two vertices in the shortest way.
    :param start: index of the first vertex.
    :param end: index of teh second vertex.
    :param matrix: matrix with lengths between vertices.
    :param free_vertices: list with vertices which are not in a cycle.
    :return: index of the vertex which connect two vertices.
    """
    length, min_length = 0, np.inf
    best_vertex = None
    vertices = [i for i in range(len(matrix)) if free_vertices[i] == 1]
    for vertex in vertices:
        length = matrix[start, vertex] + matrix[end, vertex]
        if length < min_length:
            min_length = length
            best_vertex = vertex
    return best_vertex


def extend_cycle(cycle: np.ndarray, matrix: np.ndarray, free_vertices: np.ndarray):
    """
    Add vertex which increase size of the cycle by the smallest amount.
    :param cycle: list with the vertices in the cycle.
    :param matrix: matrix with lengths between vertices.
    :param free_vertices: list with vertices which are not in a cycle.
    :return: extended cycle.
    """
    best_length = np.inf
    best_cycle = None
    added_vertex = None
    for i, (start, end) in enumerate(zip(cycle, cycle[1:])):
        new_vertex = find_the_best_vertex(start, end, matrix, free_vertices)
        new_cycle = np.concatenate([cycle[:i+1], [new_vertex], cycle[i+1:]])
        length = calculate_cycle_length(matrix, new_cycle)
        if length < best_length:
            best_length = length
            best_cycle = new_cycle
            added_vertex = new_vertex
    free_vertices[added_vertex] = 0
    return best_cycle


def greedy_cycles(matrix: np.ndarray, vertices: np.ndarray, start_ver: int = None, draw: bool = False):
    """
    Find solution for double TSP using greedy cycles approach.
    :param matrix: matrix with lengths between vertices.
    :param vertices: array with the coordinates of vertices.
    :param start_ver: optional argument, if int is passed it will be used as index of the first vertex.
    :param draw: pass True if results should be drawn, False otherwise.
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
        cycle_a = extend_cycle(cycle_a, matrix, free_vertices)
        cycle_b = extend_cycle(cycle_b, matrix, free_vertices)

    length_a = calculate_cycle_length(matrix, cycle_a)
    length_b = calculate_cycle_length(matrix, cycle_b)    
    
    if draw:
        draw_cycles([cycle_a, cycle_b], vertices)

    return length_a + length_b
