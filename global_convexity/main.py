import time
import numpy as np
import matplotlib.pyplot as plt

from random_generator import random_generator
from matrix import parse_file, create_distance_matrix
from helpers import calculate_path_length
from greedy_search import greedy_search
from metrics import edge_similarity, vertex_similarity
from tqdm import tqdm


KROA_PATH = "./data/kroa100.tsp"
KROB_PATH = "./data/krob100.tsp"


if __name__ == "__main__":

    vertices_kroa = parse_file(KROB_PATH)
    matrix = create_distance_matrix(vertices_kroa)

    sim_vertices_best = []
    sim_edges_best = []

    sim_vertices_mean = []
    sim_edges_mean = []

    quality_best = []
    quality_mean = []

    cycles = []

    for i in tqdm(range(1000)):
        cycle_a, cycle_b = random_generator(matrix, vertices_kroa)
        cycle_a, cycle_b = cycle_a[:-1], cycle_b[:-1]

        greedy_search(matrix, cycle_a, cycle_b, "edges")

        length_a, length_b = calculate_path_length(matrix, cycle_a), calculate_path_length(matrix, cycle_b)

        cycles.append({"cycle_a": list(cycle_a), "len_a": length_a, "cycle_b": list(cycle_b), "length_b": length_b, "summary": length_a + length_b})

    best_cycle = min(cycles, key=lambda x: x["summary"])

    for cycle in tqdm(cycles):
        sim_vertices_temp = []
        sim_edges_temp = []

        for temp_cycle in cycles:
            if temp_cycle == cycle:
                continue
            
            sim_vertices_temp.append(vertex_similarity(cycle["cycle_a"], cycle["cycle_b"], temp_cycle["cycle_a"], temp_cycle["cycle_b"]))
            sim_edges_temp.append(edge_similarity(cycle["cycle_a"], cycle["cycle_b"], temp_cycle["cycle_a"], temp_cycle["cycle_b"]))

        sim_vertices_mean.append(sum(sim_vertices_temp)/len(sim_vertices_temp))
        sim_edges_mean.append(sum(sim_edges_temp)/len(sim_edges_temp))
        quality_mean.append(cycle["summary"])
        
        if cycle == best_cycle:
            continue

        sim_vertices_best.append(vertex_similarity(cycle["cycle_a"], cycle["cycle_b"], best_cycle["cycle_a"], best_cycle["cycle_b"]))
        sim_edges_best.append(edge_similarity(cycle["cycle_a"], cycle["cycle_b"], best_cycle["cycle_a"], best_cycle["cycle_b"]))
        quality_best.append(cycle["summary"])

    plt.title("Podobieństwo wierzchołków do najlepszego")
    plt.xlabel("Wartość funkcji celu")
    plt.ylabel("Podobieństwo")
    plt.scatter(quality_best, sim_vertices_best)
    plt.show()

    plt.title("Podobieństwo krawędzi do najlepszego")
    plt.xlabel("Wartość funkcji celu")
    plt.ylabel("Podobieństwo")
    plt.scatter(quality_best, sim_edges_best)
    plt.show()

    plt.title("Średnie podobieństwo wierzchołków")
    plt.xlabel("Wartość funkcji celu")
    plt.ylabel("Podobieństwo")
    plt.scatter(quality_mean, sim_vertices_mean)
    plt.show()

    plt.title("Średnie podobieństwo krawędzi")
    plt.xlabel("Wartość funkcji celu")
    plt.ylabel("Podobieństwo")
    plt.scatter(quality_mean, sim_edges_mean)
    plt.show()

    print(f"Korelacja: podobieństwo wierzchołków do najlepszego wyniku: {np.corrcoef(quality_best, sim_vertices_best)[0, 1]}")
    print(f"Korelacja: podobieństwo krawędzi do najlepszego wyniku: {np.corrcoef(quality_best, sim_edges_best)[0, 1]}")
    print(f"Korelacja: średnie podobieństwo wierzchołków: {np.corrcoef(quality_mean, sim_vertices_mean)[0, 1]}")
    print(f"Korelacja: średnie podobieństwo krawędzi: {np.corrcoef(quality_mean, sim_edges_mean)[0, 1]}")
