from copy import deepcopy
import improve_operations as io
from helpers import remove_at

SWAP_EDGE, SWAP_NODE = range(2)

def lm_search(matrix, cycle_a, cycle_b):
    def next_moves(cycles, move):
        kind = move[1]
        moves = []
        if kind == SWAP_EDGE:
            _, _, a, b, c, d = move
            cycle = cycles[0] if a in cycles[0] else cycles[1]
            n = len(cycle)
            for i, j in io.gen_swap_edge(n):
                delta, a, b, c, d = io.gen_swap_edge_2(matrix, cycle, i, j)
                if delta < 0: 
                    moves.append((delta, SWAP_EDGE, a, b, c, d))
                
        elif kind == SWAP_NODE:
            _, _, c1, c2, _, y1, _, _, y2, _ = move
            i, j = list(cycles[c1]).index(y2), list(cycles[c2]).index(y1)
            n, m = len(cycles[c1]), len(cycles[c2])
            for k in range(m):
                delta, move = io.make_swap_node(matrix, cycles, c1, i, c2, k)
                if delta < 0: 
                    moves.append(move)
            for k in range(n):
                delta, move = io.make_swap_node(matrix, cycles, c2, j, c1, k)
                if delta < 0: 
                    moves.append(move)
                
        return moves

    cycles = (cycle_a, cycle_b)

    cycles = deepcopy(cycles)
    moves = sorted(io.init_moves(matrix, cycles), key=lambda x: x[0])
    
    while True:
        to_delete = []
        best_move = None
        for k, move in enumerate(moves):
            kind = move[1]
            if kind == SWAP_EDGE:
                _, _, a, b, c, d = move
                (c1, s1), (c2, s2) = io.any_has_edge(cycles, a, b), io.any_has_edge(cycles, c, d)
                if c1 != c2 or s1 == 0 or s2 == 0:
                    to_delete.append(k)
                elif s1 == s2 == +1:
                    to_delete.append(k)
                    best_move = move
                    break
                elif s1 == s2 == -1:
                    # to_delete.append(k)
                    # best_move = move[0], SWAP_EDGE, b, a, d, c
                    # break
                    continue
            elif kind == SWAP_NODE:
                _, _, c1, c2, x1, y1, z1, x2, y2, z2 = move
                s1 = io.has_edge(cycles[c1], x1, y1)
                s2 = io.has_edge(cycles[c1], y1, z1)
                s3 = io.has_edge(cycles[c2], x2, y2)
                s4 = io.has_edge(cycles[c2], y2, z2)
                
                if c1 == c2 or s1 == 0 or s2 == 0 or s3 == 0 or s4 == 0:
                    to_delete.append(k)
                elif s1 == s2 and s3 == s4:
                    to_delete.append(k)
                    best_move = move
                    break
                
        if best_move is None:
            break
            
        remove_at(moves, to_delete)
        io.apply_move(cycles, best_move)
        
        new_moves = next_moves(cycles, best_move)
        moves = sorted(list(set(moves).union(set(new_moves))), key=lambda x: x[0])
        
    return cycles