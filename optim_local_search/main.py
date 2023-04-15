from matrix import parse_file, create_distance_matrix
from search_candidates import search_candidates
from lm_search import lm_search
from steepest_search import steepest_search
from random_generator import random_generator
from helpers import calculate_path_length


KROA_PATH = "./data/kroa100.tsp"
KROB_PATH = "./data/krob100.tsp"


if __name__ == "__main__":

    vertices_kroa = parse_file(KROA_PATH)
    matrix = create_distance_matrix(vertices_kroa)

    cycle_a, cycle_b = random_generator(matrix, vertices_kroa)
    cycle_a, cycle_b = cycle_a[:-1], cycle_b[:-1]

    # steepest search
    # steepest_search(matrix, cycle_a, cycle_b, "edges")

    # length_a, length_b = calculate_path_length(matrix, cycle_a), calculate_path_length(matrix, cycle_b)
    # print(length_a, length_b)

    length_a, length_b = calculate_path_length(matrix, cycle_a), calculate_path_length(matrix, cycle_b)
    print(length_a, length_b)

    cycle_a, cycle_b = lm_search(matrix, cycle_a, cycle_b)
    
    length_a, length_b = calculate_path_length(matrix, cycle_a), calculate_path_length(matrix, cycle_b)
    print(length_a, length_b)
