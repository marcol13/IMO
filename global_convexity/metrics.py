def count_edges(cycle_a, cycle_b):
    counter = 0

    for i in range(len(cycle_a) - 1):
        for j in range(len(cycle_b) - 1):
            if cycle_a[i:i+2] == cycle_b[j:j+2]:
                counter += 1
                break
    
    return counter

def vertex_similarity(cycle_aa, cycle_ab, cycle_ba, cycle_bb):
    cycle_aa, cycle_ab, cycle_ba, cycle_bb = set(cycle_aa), set(cycle_ab), set(cycle_ba), set(cycle_bb)

    aa_bb_intersection = len(cycle_aa.intersection(cycle_ba)) + len(cycle_ab.intersection(cycle_bb))
    ab_ba_intersection = len(cycle_aa.intersection(cycle_bb)) + len(cycle_ab.intersection(cycle_ba))

    return max(aa_bb_intersection, ab_ba_intersection)

def edge_similarity(cycle_aa, cycle_ab, cycle_ba, cycle_bb):
    cycle_aa_c = cycle_aa.copy()
    cycle_ab_c = cycle_ab.copy()
    cycle_ba_c = cycle_ba.copy()
    cycle_bb_c = cycle_bb.copy()

    cycle_aa_c.append(cycle_aa_c[0])
    cycle_ab_c.append(cycle_ab_c[0])
    cycle_ba_c.append(cycle_ba_c[0])
    cycle_bb_c.append(cycle_bb_c[0])

    aa_bb_count = count_edges(cycle_aa_c, cycle_ba_c) + count_edges(cycle_ab_c, cycle_bb_c)
    ab_ba_count = count_edges(cycle_ab_c, cycle_ba_c) + count_edges(cycle_aa_c, cycle_bb_c)

    if aa_bb_count > 100 or ab_ba_count > 100:
        print(cycle_aa_c)
        print()
        print(cycle_ab_c)
        print()
        print(cycle_ba_c)
        print()
        print(cycle_bb_c)
        print()

    return max(aa_bb_count, ab_ba_count)

