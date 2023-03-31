from itertools import combinations
import numpy as np



def swap_vertices_between_cycles(cycle_a, cycle_b, vertex_a, vertex_b):
    index_a, index_b = np.where(cycle_a == vertex_a)[0], np.where(cycle_b == vertex_b)[0]
    cycle_a[index_a], cycle_b[index_b] = cycle_b[index_b], cycle_a[index_a]


def swap_vertices_inside_cycle(cycle, vertex_a, vertex_b):
    index_a, index_b = np.where(cycle == vertex_a)[0], np.where(cycle == vertex_b)[0]
    cycle[index_a], cycle[index_b] = cycle[index_b], cycle[index_a]


def swap_edges_inside_cycle(cycle, vertex_a, vertex_b):
    index_a, index_b = np.where(cycle == vertex_a)[0][0], np.where(cycle == vertex_b)[0][0]
    if index_a == 0 and index_b == len(cycle) - 1:
        cycle[index_a], cycle[index_b] = cycle[index_b], cycle[index_a]
    cycle[index_a:index_b+1] = cycle[index_a:index_b+1][::-1]


def get_pairs_for_swap_between_cycles(cycle_a, cycle_b):
    return [(i, j) for i in cycle_a for j in cycle_b]


def get_pairs_for_swap_inside_cycles(cycle_a, cycle_b):
    return list(combinations(cycle_a, 2)), list(combinations(cycle_b, 2))


def get_pairs_for_swap_inside_cycle(cycle):
    return list(combinations(cycle, 2))


def calculate_distance_diff_for_swap_between_cycles(matrix, cycle_a, cycle_b, vertex_a: int, vertex_b: int):
    change = 0
    cycle_a, cycle_b = list(cycle_a), list(cycle_b)
    index_a, index_b = cycle_a.index(vertex_a), cycle_b.index(vertex_b)
    # add new edges
    change += matrix[vertex_b][cycle_a[index_a - 1]] + matrix[vertex_b][cycle_a[(index_a + 1) % len(cycle_a)]]
    change += matrix[vertex_a][cycle_b[index_b - 1]] + matrix[vertex_a][cycle_b[(index_b + 1) % len(cycle_b)]]
    # remove existing edges
    change -= matrix[vertex_a][cycle_a[index_a - 1]] + matrix[vertex_a][cycle_a[(index_a + 1) % len(cycle_a)]]
    change -= matrix[vertex_b][cycle_b[index_b - 1]] + matrix[vertex_b][cycle_b[(index_b + 1) % len(cycle_b)]]
    return change


def calculate_distance_diff_for_swap_inside_cycle(matrix, cycle, vertex_a: int, vertex_b: int):
    change = 0
    cycle = list(cycle)
    index_a, index_b = cycle.index(vertex_a), cycle.index(vertex_b)
    # edge case explained in images/obok.png
    if abs(index_a - index_b) == 1:
        change += matrix[vertex_b][cycle[index_a - 1]] + matrix[vertex_a][cycle[(index_b + 1) % len(cycle)]]
        change -= matrix[vertex_b][cycle[index_a - 1]] + matrix[vertex_a][cycle[(index_b + 1) % len(cycle)]]
    # edge case explained in images/konce.png
    if index_a == 0 and index_b == len(cycle) - 1:
        change += matrix[vertex_a][cycle[index_b - 1]] + matrix[vertex_b][cycle[index_a + 1]]
        change -= matrix[vertex_a][cycle[index_a + 1]] + matrix[vertex_b][cycle[index_b - 1]]
    else:
        # add new edges
        change += matrix[vertex_b][cycle[index_a - 1]] + matrix[vertex_b][cycle[(index_a + 1) % len(cycle)]]
        change += matrix[vertex_a][cycle[index_b - 1]] + matrix[vertex_a][cycle[(index_b + 1) % len(cycle)]]
        # remove existing edges
        change -= matrix[vertex_a][cycle[index_a - 1]] + matrix[vertex_a][cycle[(index_a + 1) % len(cycle)]]
        change -= matrix[vertex_b][cycle[index_b - 1]] + matrix[vertex_b][cycle[(index_b + 1) % len(cycle)]]
    return change


def calculate_distance_diff_for_swap_edges(matrix, cycle, vertex_a: int, vertex_b: int):
    change = 0
    cycle = list(cycle)
    index_a, index_b = cycle.index(vertex_a), cycle.index(vertex_b)
    # edge case for swapping edges between first and last nodes
    if index_a == 0 and index_b == len(cycle) - 1:
        change += matrix[vertex_a][cycle[index_b - 1]] + matrix[vertex_b][cycle[index_a + 1]]
        change -= matrix[vertex_a][cycle[index_a + 1]] + matrix[vertex_b][cycle[index_b - 1]]
    else:
        change += matrix[vertex_a][cycle[(index_b + 1) % len(cycle)]] + matrix[vertex_b][cycle[index_a - 1]]
        change -= matrix[vertex_a][cycle[index_a - 1]] + matrix[vertex_b][cycle[(index_b + 1) % len(cycle)]]
    return change