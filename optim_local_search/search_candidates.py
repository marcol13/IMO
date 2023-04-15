import numpy as np
from copy import deepcopy

import improve_operations as io
from helpers import find_node

SWAP_EDGE, SWAP_NODE = range(2)


def search_candidates(matrix, cycle_a, cycle_b, k=10):

    cycles = (cycle_a, cycle_b)

    N = len(matrix)
    cycles = deepcopy(cycles)
    closest = np.argpartition(matrix, k+1, axis=1)[:,:k+1]
    
    while True:
        best_move, best_delta = None, 0
        for a in range(N):
            for b in closest[a]:
                if a == b: continue
                (c1, i), (c2, j) = find_node(cycles, a), find_node(cycles, b)
                move, delta = None, None
                if c1 == c2:
                    cycle = cycles[c1]
                    n = len(cycle)
                    a, b, c, d = a, cycle[(i+1)%n], b, cycle[(j+1)%n]
                    delta = io.delta_swap_edge(matrix, a, b, c, d)
                    move = delta, SWAP_EDGE, a, b, c, d
                else:
                    delta, move = io.make_swap_node(matrix, cycles, c1, i, c2, j)
                if delta < best_delta:
                    best_delta, best_move = delta, move
                    
        if best_move is None:
            break
            
        io.apply_move(cycles, best_move)
            
    return cycles