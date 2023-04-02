import numpy as np
import swap_operations as so
import time
import random


def random_search(matrix, cycle_a, cycle_b, inside_swap, time_limit=1):
    random.seed()
    start = time.time()
    while time.time() - time_limit <= start:
        is_inside = random.choice([True, False])
        if is_inside:
            cycle = random.choice([cycle_a, cycle_b])
            vertex_a, vertex_b = random.choice(so.get_pairs_for_swap_inside_cycle(cycle))
            move = random.choice([so.swap_vertices_inside_cycle, so.swap_edges_inside_cycle])
            move(cycle, vertex_a, vertex_b)
        else:
            vertex_a, vertex_b = random.choice(so.get_pairs_for_swap_between_cycles(cycle_a, cycle_b))
            so.swap_vertices_between_cycles(cycle_a, cycle_b, vertex_a, vertex_b)
            
    cycle_a = np.append(cycle_a, cycle_a[0])
    cycle_b = np.append(cycle_b, cycle_b[0])

    return cycle_a, cycle_b
            
