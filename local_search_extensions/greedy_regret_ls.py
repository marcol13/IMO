import numpy as np

def delta_insert(matrix, path, i, id):
    a, b = path[i - 1], path[i]
    return matrix[a, id] + matrix[id, b] - matrix[a, b]

def greedy_regret(matrix, paths, remaining):
    while remaining:
        for path in paths:
            scores = np.array([[delta_insert(matrix, path, i, v) for i in range(len(path))] for v in remaining])
            best_idx = None
            if scores.shape[1] == 1:
                best_idx = np.argmin(scores)
            else:
                regret = np.diff(np.partition(scores, 1)[:,:2]).reshape(-1)
                weight = regret - 0.37*np.min(scores, axis=1)
                best_idx = np.argmax(weight)
                
            best_city = remaining[best_idx]
            best_insert = np.argmin(scores[best_idx])
            path.insert(best_insert, best_city)
            remaining.remove(best_city)
    return paths