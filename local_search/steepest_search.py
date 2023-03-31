import numpy as np
import swap_operations as so


def steepest_search(matrix, cycle_a, cycle_b, swap_function):
    
    def between_cycles():
        pairs = so.get_pairs_for_swap_between_cycles(cycle_a, cycle_b)
        changes = np.array([so.calculate_distance_diff_for_swap_between_cycles(matrix, cycle_a, cycle_b, pairs[i][0], pairs[i][1]) for i in range(len(pairs))])
        if np.min(changes) >= 0:
            return 0, None, None
        vertex_a, vertex_b = np.argmin(changes)
        return np.min(changes), (vertex_a, vertex_b), so.swap_vertices_between_cycles
    
    def inside_cycles():
        stats = [check_cycle(cycle) for cycle in [cycle_a, cycle_b]]
        return stats[0] if stats[0][0] < stats[0][1] else stats[1]
        
    def check_cycle(cycle):
        pairs = so.get_pairs_for_swap_inside_cycle(cycle)
        changes = np.array([so.calculate_distance_diff_for_swap_inside_cycle(matrix, cycle_a, pairs[i][0], pairs[i][1]) for i in range(len(pairs))])
        if np.min(changes) >= 0:
            return 0, None ,None
        vertex_a, vertex_b = np.argmin(changes)
        return np.min(changes), (vertex_a, vertex_b), so.swap_vertices_inside_cycle
    
    while True:
        for func in [between_cycles, inside_cycles]:
            change, vertices, swap_func = func()
            
