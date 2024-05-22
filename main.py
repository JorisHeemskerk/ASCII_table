import numpy as np

import ASCII_table

def generate_random_matrix(
    rows: int, 
    cols: int, 
    tuple_size: int, 
    low: int, 
    high: int
):
    """
    Generates a numpy matrix of defined size containing tuples of random integers.

    Parameters:
    - rows: Number of rows in the matrix.
    - cols: Number of columns in the matrix.
    - tuple_size: Number of integers in each tuple.
    - low: The lowest integer (inclusive) that can be in the tuple.
    - high: The highest integer (exclusive) that can be in the tuple.

    Returns:
    - A numpy matrix of the defined size with tuples of random integers.
    """
    matrix = np.empty((rows, cols), dtype=object)
    for i in range(rows):
        for j in range(cols):
            matrix[i, j] = tuple(np.random.randint(low, high-1) for _ in range(tuple_size))
    return matrix

def generate_random_colours_matrix(rows: int, cols: int):
    """
    Generates a numpy matrix of defined size containing random Colours enum values.

    Parameters:
    - rows: Number of rows in the matrix.
    - cols: Number of columns in the matrix.

    Returns:
    - A numpy matrix of the defined size with random Colours enum values.
    """
    colours_list = list(ASCII_table.Colours)
    matrix = np.empty((rows, cols), dtype=object)
    for i in range(rows):
        for j in range(cols):
            matrix[i, j] = np.random.choice(colours_list)
    return matrix


def main():
    matrix = [
        [('^', '<   >', 'v'),('^', '<   >', 'v'),('^', '<   >', 'v'),('^', '<   >', 'v')],
        [('^', '<   >', 'v'),('^', '<   >', 'v'),('^', '<   >', 'v'),('^', '', 'v')],
        [('^', '<   >', 'v'),('^', '<   >', 'v'),('^', '<   >', 'v'),('^', '<   >', 'v')],
        [('^', '<   >' ),('^', '<   >', 'v'),('^', '<   >', 'v'),('^', '<   >', 'v')]
    ]
    matrix = generate_random_matrix(rows=3, cols=11, tuple_size=2, low=-10, high=10)
    # matrix = generate_random_matrix(rows=3, cols=11, tuple_size=4, low=-100, high=100)
    # colour_matrix = generate_random_colours_matrix(len(matrix), len(matrix[0]))
    a = ASCII_table.ASCIITable(matrix)
    a.change_colour((1,3), ASCII_table.Colours.DARK_YELLOW)
    print(matrix)
    print(a)

if __name__ == "__main__":
    main()
