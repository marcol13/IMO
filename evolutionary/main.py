from ils import ils_run
from msls import msls_run
from matrix import parse_file, create_distance_matrix
from evolutionary import Evolutionary


KROA_PATH = "./data/krob100.tsp"
KROB_PATH = "./data/krob100.tsp"


if __name__ == "__main__":

    vertices_kroa = parse_file(KROA_PATH)
    matrix = create_distance_matrix(vertices_kroa)

    evo = Evolutionary(vertices_kroa, matrix)

    print(evo.evolutionary_search(matrix, vertices_kroa, local_search=True))



