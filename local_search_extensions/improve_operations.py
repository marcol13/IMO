import random
from helpers import reverse, find_node

SWAP_EDGE, SWAP_NODE = range(2)


def delta_swap_node(D, x1, y1, z1, x2, y2, z2):
    x1, y2 = int(x1), int(y2)
    return D[x1,y2] + D[z1,y2] - D[x1,y1] - D[z1,y1] + D[x2,y1] + D[z2,y1] - D[x2,y2] - D[z2,y2]

def make_swap_node(cities, cycles, cyc1, i, cyc2, j, calc_delta=True):
    C1, C2 = cycles[cyc1], cycles[cyc2]
    D = cities
    n, m = len(C1), len(C2)
    x1, y1, z1 = C1[(i-1)%n], C1[i], C1[(i+1)%n]
    x2, y2, z2 = C2[(j-1)%m], C2[j], C2[(j+1)%m]
    delta = delta_swap_node(cities, x1, y1, z1, x2, y2, z2) if calc_delta else 0
    move = delta, SWAP_NODE, cyc1, cyc2, x1, y1, z1, x2, y2, z2
    return delta, move

def delta_swap_edge(cities, a, b, c, d):
    if a == d or a == b or a == c or b == c or b == d or c == d: 
        return 1e8
    return cities[a, c] + cities[b, d] - cities[a, b] - cities[c, d]

def gen_swap_edge_2(cities, cycle, i, j, calc_delta=True):
    n = len(cycle)
    nodes = cycle[i], cycle[(i+1)%n], cycle[j], cycle[(j+1)%n]
    return (delta_swap_edge(cities, *nodes), *nodes) if calc_delta else (0, *nodes)

def gen_swap_edge(n):
    return [(i, (i+d)%n) for i in range(n) for d in range(2, n-1)]

def gen_swap_node(n, m):
    return [(i, j) for i in range(n) for j in range(m)]


def get_first_edge_swap(cities, cycles, better):
    for k in random.sample(range(2), 2):
        cycle = cycles[k]
        n = len(cycle)
        candidates = gen_swap_edge(n)
        random.shuffle(candidates)
        for i, j in candidates:
            delta, a, b, c, d = gen_swap_edge_2(cities, cycle, i, j, calc_delta=better)
            if not (delta >= 0 and better):
                return (delta, SWAP_EDGE, a, b, c, d)
    return None

def get_first_node_swap(cities, cycles, better):
    candidates = gen_swap_node(len(cycles[0]), len(cycles[1]))
    random.shuffle(candidates)
    for i, j in candidates:
        delta, move = make_swap_node(cities, cycles, 0, i, 1, j, calc_delta=better)
        if not (delta >= 0 and better): 
            return move
    return None
        
def get_move(cities, cycles, calc_delta=True):
    moves = [get_first_edge_swap, get_first_node_swap]
    move_order = random.sample(range(2), 2)
    move = moves[move_order[0]](cities, cycles, calc_delta)
    if move is None: 
        move = moves[move_order[1]](cities, cycles, calc_delta)
    return move

def apply_move(cycles, move):
    kind = move[1]
    if kind == SWAP_EDGE:
        _, _, a, _, c, _ = move
        (c1, i), (c2, j) = find_node(cycles, a), find_node(cycles, c)
        cycle = cycles[c1]
        n = len(cycle)
        reverse(cycle, (i+1)%n, j)
    elif kind == SWAP_NODE:
        _, _, c1, c2, _, a, _, _, b, _ = move
        i, j = cycles[c1].index(a), cycles[c2].index(b)
        cycles[c1][i], cycles[c2][j] = cycles[c2][j], cycles[c1][i]
    else:
        assert False, 'Invalid move type'
