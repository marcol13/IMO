import time
import numpy as np

from greedy_regret import greedy_regret
from matrix import parse_file, create_distance_matrix
from helpers import calculate_path_length, draw_cycles
from steepest_search import steepest_search


KROA_PATH = "./local_search/data/kroa100.tsp"
KROB_PATH = "./local_search/data/krob100.tsp"


if __name__ == "__main__":

    vertices_kroa = parse_file(KROB_PATH)
    matrix = create_distance_matrix(vertices_kroa)

    # TODO add runs for random search and unchanged solution

    # TODO add greedy search
    for local_search in [steepest_search]:
        for inside_swap in ["vertices", "edges"]:
            times = []
            lengths = []

            for i in range(100):
                cycle_a, cycle_b = greedy_regret(matrix, vertices_kroa, i)
                cycle_a, cycle_b = cycle_a[:-1], cycle_b[:-1]

                start = time.time()
                local_search(matrix, cycle_a, cycle_b, inside_swap)
                times.append(time.time() - start)
                
                length_a, length_b = calculate_path_length(matrix, cycle_a), calculate_path_length(matrix, cycle_b)
                lengths.append(length_a + length_b)

            print(local_search.__name__, inside_swap)
            print(f"Lenghts: {min(lengths)}, {np.mean(lengths)}, {max(lengths)}")
            print(f"Times: {min(times)}, {np.mean(times)}, {max(times)}")
            print(f"The best results for intial vertex {np.argmin(lengths)}")
