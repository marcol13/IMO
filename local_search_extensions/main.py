from ils import ils_run
from msls import msls_run
from matrix import parse_file, create_distance_matrix


KROA_PATH = "./data/krob100.tsp"
KROB_PATH = "./data/krob100.tsp"


if __name__ == "__main__":

    vertices_kroa = parse_file(KROA_PATH)
    matrix = create_distance_matrix(vertices_kroa)

    print(msls_run(matrix, vertices_kroa, num_iterations=2))

    print(ils_run(matrix, vertices_kroa, "ils2", 10))



