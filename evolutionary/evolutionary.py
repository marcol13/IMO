from copy import deepcopy
from tqdm import tqdm
from time import time
from helpers import *

import numpy as np

import random
import random_generator
import greedy_regret
import greedy_search

class Evolutionary:
    def __init__(self, cities, coords):
        self.cities, self.coords = cities, coords

    def combine(self, solution_1, solution_2):
        solution_1, solution_2 = deepcopy(solution_1), deepcopy(solution_2)
        
        remaining = []
        for cycle_1 in solution_1:
            n = len(cycle_1)
            if n == 1:
                continue
            for i in range(n):
                p, q = cycle_1[i], cycle_1[(i+1)%n]
                if p == -1 or q == -1 or p == q:
                    continue
                found = False
                for cycle_2 in solution_2:
                    m = len(cycle_2)
                    for j in range(m):
                        u, v = cycle_2[j], cycle_2[(j+1)%m]
                        if (p == u and q == v) or (p == v and q == u):
                            found = True
                            break
                    if found:
                        break
                        
                if not found:
                    remaining.append(cycle_1[i])
                    remaining.append(cycle_1[(i+1)%n])
                    cycle_1[i] = -1
                    cycle_1[(i+1)%n] = -1
                    
            for i in range(1, n):
                x, y, z = cycle_1[(i-1)%n], cycle_1[i], cycle_1[(i+1)%n]
                if x == z == -1 and y != -1:
                    remaining.append(y)
                    cycle_1[i] = -1
                    
            for i in range(1, n):
                x = cycle_1[i]
                if x != -1 and np.random.rand() < 0.2:
                    remaining.append(x)
                    cycle_1[i] = -1
                    
        a = [x for x in solution_1[0] if x != -1]
        b = [x for x in solution_1[1] if x != -1]
        assert len(a) + len(b) + len(remaining) == 200
        return greedy_regret(self.cities, (a, b), remaining)[1]
    
    def perturb(self, cycles, strength=0.2):
        to_destroy = int(strength*len(self.cities)/2)
        
        remaining = []
        for cycle in cycles:
            n = len(cycle)
            destroy_begin = random.randint(0, n - 1)
            remaining.extend(cycle[destroy_begin : destroy_begin + to_destroy])
            cycle[destroy_begin : destroy_begin + to_destroy] = []

            if destroy_begin + to_destroy > n:
                remaining.extend(cycle[0 : destroy_begin + to_destroy - n])
                cycle[0 : destroy_begin + to_destroy - n] = []
    
        return greedy_regret(self.cities, cycles, remaining)[1]
    
    def evolutionary_search(self, *, pop_size=20, min_diff=40, plot=False, patience=300, local_search=True):
        local_search = greedy_search(self.cities)
        pop = [local_search(random_generator(len(self.cities)))[1] for _ in tqdm(range(pop_size))]
        pop = [(x, calculate_path_length(self.cities, x)) for x in pop]
        best_scores = []
        worst_scores = []
        
        iteration = last_improv = 0
        last_best = pop[0][1]
        best_idx = 0
        while True:
            iteration += 1
            
            pop_idx = np.arange(len(pop))
            np.random.shuffle(pop_idx)

            worst_idx = np.argmax(pop, lambda x: x[1])
            _, worst_score = pop[worst_idx]

            avg_score = np.mean([i[1] for i in pop])
            solution_1, solution_1_score = pop[pop_idx[0]]
            solution_2, solution_2_score = pop[pop_idx[1]]
            sol = self.combine(solution_1, solution_2)
            if local_search:
                sol = local_search(sol, inplace=True)[1]
            sol_score = calculate_path_length(self.cities, sol)
            print(f'{solution_1_score} + {solution_2_score} -> {sol_score}')
            
            too_similar = any(abs(sol_score - s) < min_diff for _, s in pop)
            if sol_score < last_best:
                pop[best_idx] = sol, sol_score
            elif sol_score < worst_score and not too_similar:
                pop[worst_idx] = sol, sol_score

            best_idx = np.argmin(pop, lambda x: x[1])
            best_sol, best_score = pop[best_idx]
            best_scores.append(best_score)
            worst_scores.append(worst_score)
            
            if best_score < last_best:
                last_best = best_score
                last_improv = iteration
                    
            if iteration - last_improv > patience:
                break

            if plot and iteration % 20 == 0:
                plt.figure()
                draw_cycles(self.coords, best_sol)
                print(f'iteration {iteration} (best: {best_score}, worst: {worst_score}, avg: {avg_score})')
                    
        if plot:
            plt.figure()
            draw_cycles(self.coords, best_sol)
            print(f'iteration {iteration} (best: {best_score}, worst: {worst_score}, avg: {avg_score})')

            
        return best_sol