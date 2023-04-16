import time
import numpy as np

from matrix import parse_file, create_distance_matrix
from search_candidates import search_candidates
from lm_search import lm_search
from steepest_search import steepest_search
from random_generator import random_generator
from helpers import calculate_path_length, draw_cycles
from greedy_regret import greedy_regret
from tqdm import tqdm


KROA_PATH = "./data/kroa200.tsp"
KROB_PATH = "./data/krob200.tsp"


if __name__ == "__main__":

    vertices_kroa = parse_file(KROB_PATH)
    matrix = create_distance_matrix(vertices_kroa)

    algorithms = [lm_search, search_candidates]

    for alg in algorithms:
        times = []
        lengths = []
        best_cycles = None
        for i in tqdm(range(100)):
            cycle_a, cycle_b = random_generator(matrix, vertices_kroa, i)
            cycle_a, cycle_b = cycle_a[:-1], cycle_b[:-1]

            start = time.time()
            cycle_a, cycle_b = alg(matrix, cycle_a, cycle_b)
            times.append(time.time() - start)

            length_a, length_b = calculate_path_length(matrix, cycle_a), calculate_path_length(matrix, cycle_b)
            
            if best_cycles == None or length_a + length_b < min(lengths):
                cycle_a = np.append(cycle_a, cycle_a[0])
                cycle_b = np.append(cycle_b, cycle_b[0])
                best_cycles = (cycle_a, cycle_b)

            lengths.append(length_a + length_b)


        print(f"Lengths: {min(lengths)}, {np.mean(lengths)}, {max(lengths)}")
        print(f"Times: {min(times)}, {np.mean(times)}, {max(times)}")

        draw_cycles(best_cycles, vertices_kroa)
