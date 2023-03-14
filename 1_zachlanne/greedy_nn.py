import random
import numpy as np

from helpers import calculate_path_length, draw_cycles


def find_the_best_vertex(start: int, end: int, matrix: np.ndarray, free_vertices: np.ndarray):
    """
    For the given points find vertex which connect two vertices in the shortest way.
    :param start: index of the first vertex.
    :param end: index of teh second vertex.
    :param matrix: matrix with lengths between vertices.
    :param free_vertices: list with vertices which are not in a cycle.
    :return: index of the vertex which connect two vertices.
    """
    min_length = np.inf
    best_vertex = None
    vertices = [i for i in range(len(matrix)) if free_vertices[i] == 1]
    # check extending path by adding new vertex at the beginning of the path
    if start == -1:
        for vertex in vertices:
            length = matrix[start, vertex]
            if length < min_length:
                min_length = length
                best_vertex = vertex
    # check extending path by adding new vertex at the end of the path
    elif end == -1:
        for vertex in vertices:
            length = matrix[end, vertex]
            if length < min_length:
                min_length = length
                best_vertex = vertex
    # check extending path by breaking connection and add new vertex between two
    else:
        for vertex in vertices:
            length = matrix[start, vertex] + matrix[end, vertex]
            if length < min_length:
                min_length = length
                best_vertex = vertex
    return best_vertex


def extend_path(path: np.ndarray, matrix: np.ndarray, free_vertices: np.ndarray):
    """
    Add vertex which increase size of the path by the smallest amount.
    :param path: list with the vertices in the path.
    :param matrix: matrix with lengths between vertices.
    :param free_vertices: list with vertices which are not in a path.
    :return: extended path.
    """
    best_length = np.inf
    best_path = None
    added_vertex = None
    # add two artificial vertices to check connection at the end and at the beginning of the path
    tmp_path = np.concatenate(([-1], path, [-1]))
    for i, (start, end) in enumerate(zip(tmp_path, tmp_path[1:])):
        new_vertex = find_the_best_vertex(start, end, matrix, free_vertices)
        new_path = np.concatenate([tmp_path[:i+1], [new_vertex], tmp_path[i+1:]])
        new_path = new_path[1:-1] # remove artificial vertices
        length = calculate_path_length(matrix, new_path)
        if length < best_length:
            best_length = length
            best_path = new_path
            added_vertex = new_vertex
    free_vertices[added_vertex] = 0
    return best_path


def greedy_nearest_neighbour(matrix: np.ndarray, vertices: np.ndarray, start_ver: int = None, draw: bool = False):
    """
    Find solution for double TSP using greedy nearest neighbour approach.
    :param matrix: matrix with lengths between vertices.
    :param vertices: array with the coordinates of vertices.
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

    path_a = np.array([start_ver_a])
    path_b = np.array([start_ver_b])

    while sum(free_vertices) > 0:
        path_a = extend_path(path_a, matrix, free_vertices)
        path_b = extend_path(path_b, matrix, free_vertices)

    length_a = calculate_path_length(matrix, path_a)
    length_b = calculate_path_length(matrix, path_b)

    cycle_a = np.concatenate((path_a, [path_a[0]]))
    cycle_b = np.concatenate((path_b, [path_b[0]]))
        
    if draw:
        draw_cycles([cycle_a, cycle_b], vertices)

    return length_a + length_b
