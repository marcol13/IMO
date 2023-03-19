import re
import math
import numpy as np


def calculate_distance(start: list[int, int], end: list[int, int]):
    return math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)


def parse_file(path: str):
    vertices = []
    
    with open(path) as f:
        lines = f.readlines()
        
    for line in lines:
        if not re.match(r"^[A-Z]", line):
            line = re.sub("\n", "", line)
            line = list(map(int, line.split(" ")[1:]))
            vertices.append(line)
        
    return np.array(vertices)


def create_distance_matrix(vertices: list):
    matrix = []
    
    for start in vertices:
        temp = []
        for end in vertices: 
            temp.append(calculate_distance(start, end))
        matrix.append(temp)
        
    return np.array(matrix)


if __name__ == "__main__":
    vertices = parse_file("./data/kroa100.tsp")
    matrix = create_distance_matrix(vertices)
    print(matrix.shape)