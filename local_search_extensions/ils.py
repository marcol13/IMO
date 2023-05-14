import copy
import time
import random
from random_generator import random_generator
from improve_operations import get_move, apply_move
from helpers import calculate_path_length
from greedy_regret_ls import greedy_regret


def greedy_search(cycles, matrix):
    cycles_copy = copy.deepcopy(cycles)
    while True:
        move = get_move(matrix, cycles_copy)
        if move is None: 
            break
        apply_move(cycles_copy, move)
    return cycles_copy


def ils1_pertubation(matrix, cycles):
    for _ in range(15):
          move = get_move(matrix, cycles, False)
          apply_move(cycles, move)
    return cycles


def ils2_pertubation(matrix, cycles):
    destroy = 0.2 * len(matrix) / 2
    destroy = int(destroy)
    remaining = []
    for cycle in cycles:
        n = len(cycle)
        destroy_begin = random.randint(0, n - 1)
        remaining.extend(cycle[destroy_begin : destroy_begin + destroy])
        cycle[destroy_begin : destroy_begin + destroy] = []

        if destroy_begin + destroy > n:
            remaining.extend(cycle[0 : destroy_begin + destroy - n])
            cycle[0 : destroy_begin + destroy - n] = []

    cycles = greedy_regret(matrix, cycles, remaining)
    
    return cycles


def ils_run(matrix, vertices, pertubation_method, max_time, local_search=False):
    if pertubation_method == "ils1":
         pertubation = ils1_pertubation
    else:
         pertubation = ils2_pertubation
    random_cycles = random_generator(matrix, vertices)
    best_cycles = greedy_search(random_cycles, matrix)
    length_a = calculate_path_length(matrix, best_cycles[0])
    length_b = calculate_path_length(matrix, best_cycles[1])
    length = length_a + length_b
    start = time.time()
    while time.time()-start < max_time:
            cycles = copy.deepcopy(best_cycles)
            cycles = pertubation(matrix, cycles)
            if local_search:
                cycles = greedy_search(cycles, matrix)
            length_a = calculate_path_length(matrix, cycles[0])
            length_b = calculate_path_length(matrix, cycles[1])
            new_length = length_a + length_b
            if new_length < length:
                best_cycles = cycles
                length = new_length
    return length
