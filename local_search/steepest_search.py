import numpy as np
import swap_operations as so
from helpers import calculate_path_length, Improvement


def steepest_search(matrix, cycle_a, cycle_b, inside_swap):

    if inside_swap == "vertices":
        swap_inside = so.swap_vertices_inside_cycle
    else:
        swap_inside = so.swap_edges_inside_cycle
    
    def between_cycles():
        pairs = so.get_pairs_for_swap_between_cycles(cycle_a, cycle_b)
        changes = np.array([so.calculate_distance_diff_for_swap_between_cycles(matrix, cycle_a, cycle_b, pairs[i][0], pairs[i][1]) for i in range(len(pairs))])
        if np.min(changes) >= 0:
            return Improvement(0, None, None)
        vertex_a, vertex_b = pairs[np.argmin(changes)]
        return Improvement(np.min(changes), (cycle_a, cycle_b, vertex_a, vertex_b), so.swap_vertices_between_cycles)
    
    def inside_cycles():
        stats = [check_cycle(cycle) for cycle in [cycle_a, cycle_b]]
        return stats[0] if stats[0].change < stats[1].change else stats[1]
        
    def check_cycle(cycle):
        pairs = so.get_pairs_for_swap_inside_cycle(cycle)
        changes = np.array([so.calculate_distance_diff_for_swap_inside_cycle(matrix, cycle, pairs[i][0], pairs[i][1]) for i in range(len(pairs))])
        if np.min(changes) >= 0:
            return Improvement(0, None, None)
        vertex_a, vertex_b = pairs[np.argmin(changes)]
        return Improvement(np.min(changes), (cycle, vertex_a, vertex_b), swap_inside)
    
    while True:
        between = between_cycles()
        inside = inside_cycles()
        if between.change >= 0 and inside.change >= 0:
            break
        if between.change < inside.change:
            print(f"Between: {calculate_path_length(matrix, cycle_a)}, {calculate_path_length(matrix, cycle_b)}, {between.change}")
            between.function(*between.args)
        else:
            print(f"Inside: {calculate_path_length(matrix, cycle_a)}, {calculate_path_length(matrix, cycle_b)}, {inside.change}")
            inside.function(*inside.args)
