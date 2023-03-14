import numpy as np

from greedy_cycle import greedy_cycles
from greedy_nn import greedy_nearest_neighbour
from matrix import parse_file, create_distance_matrix

KROA_PATH = "1_zachlanne/data/kroa100.tsp"
KROB_PATH = "1_zachlanne/data/krob100.tsp"
RESULTS_FILE_PATH = "1_zachlanne/data/results.txt"

if __name__ == "__main__":

    # create instances
    vertices_kroa = parse_file(KROA_PATH)
    matrix_kroa = create_distance_matrix(vertices_kroa)

    vertices_krob = parse_file(KROB_PATH)
    matrix_krob = create_distance_matrix(vertices_krob)

    # greedy nearest neighbour
    kroa_nn = [greedy_nearest_neighbour(matrix_kroa, vertices_kroa, i) for i in range(100)]
    krob_nn = [greedy_nearest_neighbour(matrix_krob, vertices_kroa, i) for i in range(100)]

    # greedy cycles
    kroa_cycles = [greedy_cycles(matrix_kroa, vertices_kroa, i) for i in range(100)]
    krob_cycles = [greedy_cycles(matrix_krob, vertices_kroa, i) for i in range(100)]

    # TODO regret

    with open(RESULTS_FILE_PATH, "w") as f:
        f.write("Greedy Nearest Neighbour:")
        f.write(f"\nKROA: max={np.max(kroa_nn)}, min={np.min(kroa_nn)}, mean={np.mean(kroa_nn)}")
        f.write(f"\nKROB: max={np.max(krob_nn)}, min={np.min(krob_nn)}, mean={np.mean(krob_nn)}")
        f.write("\nGreedy Cycles:")
        f.write(f"\nKROA: max={np.max(kroa_cycles)}, min={np.min(kroa_cycles)}, mean={np.mean(kroa_cycles)}")
        f.write(f"\nKROB: max={np.max(krob_cycles)}, min={np.min(krob_cycles)}, mean={np.mean(krob_cycles)}")


    # start from random vertex and generate plots
    greedy_nearest_neighbour(matrix_kroa, vertices_kroa, draw=True)
    greedy_nearest_neighbour(matrix_krob, vertices_krob, draw=True)
    greedy_cycles(matrix_kroa, vertices_kroa, draw=True)
    greedy_cycles(matrix_krob, vertices_krob, draw=True)
