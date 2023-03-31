from itertools import combinations
import numpy as np

from greedy_regret import greedy_regret
from matrix import parse_file, create_distance_matrix
from helpers import calculate_path_length, draw_cycles


KROA_PATH = "./local_search/data/kroa100.tsp"
KROB_PATH = "./local_search/data/krob100.tsp"

def swap_vertices_between_cycles(cycle_a, cycle_b):
    changes = get_pairs_for_swap_between_cycles(cycle_a, cycle_b)
    a = np.array([calculate_distance_diff_for_swap_between_cycles(matrix, cycle_a, cycle_b, changes[i][0], changes[i][1]) for i in range(len(changes))])
    if np.min(a) >= 0:
        return 1
    vertex_a, vertex_b = changes[np.argmin(a)]
    index_a, index_b = np.where(cycle_a == vertex_a)[0], np.where(cycle_b == vertex_b)[0]
    cycle_a[index_a], cycle_b[index_b] = cycle_b[index_b], cycle_a[index_a]
    return np.min(a)

def swap_vertices_inside_cycle(cycle_a, cycle_b):
    changes_a, changes_b = get_pairs_for_swap_inside_cycles(cycle_a, cycle_b)
    a = np.array([calculate_distance_diff_for_swap_inside_cycle(matrix, cycle_a, changes_a[i][0], changes_a[i][1]) for i in range(len(changes_a))])
    b = np.array([calculate_distance_diff_for_swap_inside_cycle(matrix, cycle_b, changes_b[i][0], changes_b[i][1]) for i in range(len(changes_b))])
    print(np.min(a), np.min(b))
    if np.min(a) == 0 and np.min(b) == 0:
        return 1
    if np.min(a) < 0:
        vertex_a, vertex_b = changes_a[np.argmin(a)]
        index_a, index_b = np.where(cycle_a == vertex_a)[0], np.where(cycle_a == vertex_b)[0]
        cycle_a[index_a], cycle_a[index_b] = cycle_a[index_b], cycle_a[index_a]
    if np.min(b) < 0:
        vertex_a, vertex_b = changes_b[np.argmin(b)]
        index_a, index_b = np.where(cycle_b == vertex_a)[0], np.where(cycle_b == vertex_b)[0]
        cycle_b[index_a], cycle_b[index_b] = cycle_b[index_b], cycle_b[index_a]
    return np.min(a) + np.min(b)

def swap_vertices_between_cycles(cycle_a, cycle_b, vertex_a, vertex_b):
    index_a, index_b = np.where(cycle_a == vertex_a)[0], np.where(cycle_b == vertex_b)[0]
    cycle_a[index_a], cycle_b[index_b] = cycle_b[index_b], cycle_a[index_a]
    return np.min(a)

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
    

if __name__ == "__main__":

    vertices_kroa = parse_file(KROA_PATH)
    matrix = create_distance_matrix(vertices_kroa)

    cycle_a, cycle_b = greedy_regret(matrix, vertices_kroa)
    cycle_a, cycle_b = cycle_a[:-1], cycle_b[:-1]

    print(cycle_a, cycle_b)

    length_a, length_b = calculate_path_length(matrix, cycle_a), calculate_path_length(matrix, cycle_b)

    print(length_a, length_b)

    draw_cycles([cycle_a, cycle_b], vertices_kroa)

    # while True:
    #     delta = swap_vertices_between_cycles(cycle_a, cycle_b)
    #     print(delta)
    #     if delta > 0:
    #         break

    # while True:
    #     delta = swap_vertices_inside_cycle(cycle_a, cycle_b)
    #     print(delta)
    #     if delta > 0:
    #         break
    while True:
        changes_a, changes_b = get_pairs_for_swap_inside_cycles(cycle_a, cycle_b)
        a = np.array([calculate_distance_diff_for_swap_edges(matrix, cycle_a, changes_a[i][0], changes_a[i][1]) for i in range(len(changes_a))])
        b = np.array([calculate_distance_diff_for_swap_edges(matrix, cycle_b, changes_b[i][0], changes_b[i][1]) for i in range(len(changes_b))])
        print(np.min(a), np.min(b))
        if np.min(a) == 0 and np.min(b) == 0:
            break
        if np.min(a) < 0:
            vertex_a, vertex_b = changes_a[np.argmin(a)]
            index_a, index_b = np.where(cycle_a == vertex_a)[0][0], np.where(cycle_a == vertex_b)[0][0]
            if index_a == 0 and index_b == len(cycle_a) - 1:
                cycle_a[index_a], cycle_a[index_b] = cycle_a[index_b], cycle_a[index_a]
            cycle_a[index_a:index_b+1] = cycle_a[index_a:index_b+1][::-1]
        if np.min(b) < 0:
            vertex_a, vertex_b = changes_b[np.argmin(b)]
            index_a, index_b = np.where(cycle_b == vertex_a)[0][0], np.where(cycle_b == vertex_b)[0][0]
            if index_a == 0 and index_b == len(cycle_a) - 1:
                cycle_b[index_a], cycle_b[index_b] = cycle_b[index_b], cycle_b[index_a]
            cycle_b[index_a:index_b+1] = cycle_b[index_a:index_b+1][::-1]

        length_a, length_b = calculate_path_length(matrix, cycle_a), calculate_path_length(matrix, cycle_b)

        print(length_a, length_b)

    draw_cycles([cycle_a, cycle_b], vertices_kroa)


