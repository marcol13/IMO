import copy
from random_generator import random_generator
from improve_operations import get_move, apply_move
from helpers import calculate_path_length


def greedy_search(cycles, matrix):
    cycles_copy = copy.deepcopy(cycles)
    while True:
        move = get_move(matrix, cycles_copy)
        if move is None: 
            break
        apply_move(cycles_copy, move)
    return cycles_copy

def msls_run(matrix, vertices, num_iterations):
    scores = []
    for _ in range(num_iterations):
        random_cycles = random_generator(matrix, vertices)
        solution = greedy_search(random_cycles, matrix)
        length_a, length_b = calculate_path_length(matrix, solution[0]), calculate_path_length(matrix, solution[1])
        scores.append(length_a + length_b)
    return scores

        