from itertools import combinations
import numpy as np

from greedy_regret import greedy_regret
from matrix import parse_file, create_distance_matrix
from helpers import calculate_path_length, draw_cycles
from steepest_search import steepest_search


KROA_PATH = "./local_search/data/kroa100.tsp"
KROB_PATH = "./local_search/data/krob100.tsp"


if __name__ == "__main__":

    vertices_kroa = parse_file(KROA_PATH)
    matrix = create_distance_matrix(vertices_kroa)

    cycle_a, cycle_b = greedy_regret(matrix, vertices_kroa)
    cycle_a, cycle_b = cycle_a[:-1], cycle_b[:-1]
    print(cycle_a, cycle_b)

    length_a, length_b = calculate_path_length(matrix, cycle_a), calculate_path_length(matrix, cycle_b)
    print(length_a, length_b)

    # draw_cycles([cycle_a, cycle_b], vertices_kroa)

    steepest_search(matrix, cycle_a, cycle_b, "vertices")

    length_a, length_b = calculate_path_length(matrix, cycle_a), calculate_path_length(matrix, cycle_b)
    print(length_a, length_b)

    # draw_cycles([cycle_a, cycle_b], vertices_kroa)
