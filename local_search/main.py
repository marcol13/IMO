import time
import numpy as np

from greedy_regret import greedy_regret
from random_generator import random_generator
from matrix import parse_file, create_distance_matrix
from helpers import calculate_path_length
from steepest_search import steepest_search
from greedy_search import greedy_search
from random_search import random_search
from tqdm import tqdm


KROA_PATH = "./local_search/data/kroa100.tsp"
KROB_PATH = "./local_search/data/krob100.tsp"


if __name__ == "__main__":

    vertices_kroa = parse_file(KROA_PATH)
    matrix = create_distance_matrix(vertices_kroa)

    # TODO add runs for unchanged solution


    for generator in [random_generator, greedy_regret]:
        for local_search in [steepest_search, greedy_search, random_search]:
            for inside_swap in ["vertices", "edges"]:
                times = []
                lengths = []

                if local_search.__name__ == random_search.__name__ and generator.__name__ == random_generator.__name__ \
                    or local_search.__name__ == random_search.__name__ and inside_swap == "edges":
                    continue

                for i in tqdm(range(100)):
                    cycle_a, cycle_b = generator(matrix, vertices_kroa, i)
                    cycle_a, cycle_b = cycle_a[:-1], cycle_b[:-1]

                    start = time.time()
                    local_search(matrix, cycle_a, cycle_b, inside_swap)
                    times.append(time.time() - start)
                    
                    length_a, length_b = calculate_path_length(matrix, cycle_a), calculate_path_length(matrix, cycle_b)
                    lengths.append(length_a + length_b)

                print(generator.__name__, local_search.__name__, inside_swap)
                print(f"Lenghts: {min(lengths)}, {np.mean(lengths)}, {max(lengths)}")
                print(f"Times: {min(times)}, {np.mean(times)}, {max(times)}")
                print(f"The best results for intial vertex {np.argmin(lengths)}")
