import numpy as np
import random
import swap_operations as so
from helpers import Improvement



def greedy_search(matrix, cycle_a, cycle_b, inside_swap):

    if inside_swap == "vertices":
        swap_inside = so.swap_vertices_inside_cycle
        distance_cal = so.calculate_distance_diff_for_swap_inside_cycle
    elif inside_swap == "edges":
        swap_inside = so.swap_edges_inside_cycle
        distance_cal = so.calculate_distance_diff_for_swap_edges
    else:
        raise ValueError("Inside swap should have value: vertices or edges!")
    
    def between_cycles():
        pairs = so.get_pairs_for_swap_between_cycles(cycle_a, cycle_b)
        random.shuffle(pairs)
        for i in range(len(pairs)):
            change = so.calculate_distance_diff_for_swap_between_cycles(matrix, cycle_a, cycle_b, pairs[i][0], pairs[i][1])  
            if change < 0:
                vertex_a, vertex_b = pairs[i][0], pairs[i][1]
                return Improvement(change, (cycle_a, cycle_b, vertex_a, vertex_b), so.swap_vertices_between_cycles)
        return Improvement(0, None, None)
    
    def inside_cycles():
        stats = [check_cycle(cycle) for cycle in [cycle_a, cycle_b]]
        return stats[0] if stats[0].change < stats[1].change else stats[1]
        
    def check_cycle(cycle):
        pairs = so.get_pairs_for_swap_inside_cycle(cycle)
        random.shuffle(pairs)
        for i in range(len(pairs)):
            change = distance_cal(matrix, cycle, pairs[i][0], pairs[i][1])  
            if change < 0:
                vertex_a, vertex_b = pairs[i][0], pairs[i][1]
                return Improvement(change, (cycle, vertex_a, vertex_b), swap_inside)
        return Improvement(0, None, None)
    
    while True:
        between = between_cycles()
        inside = inside_cycles()
        if between.change >= 0 and inside.change >= 0:
            break
        first_method = random.randint(1, 2)
        if first_method == 1:
            if between.change < 0:
                between.function(*between.args)
            else:
                inside.function(*inside.args)
        else:
            if inside.change < 0:
                inside.function(*inside.args)
            else:
                between.function(*between.args)
