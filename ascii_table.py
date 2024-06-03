import numpy as np
from typing import TypeVar, Generic

from .colours import Colours

T = TypeVar("T")

class ASCIITable(Generic[T]):
    """
    ASCIITable class.
    """

    def __init__(
        self, 
        data: list[list[T]] | np.ndarray, 
        colour_matrix: np.ndarray=None
    )-> None:
        self.data = data
        if colour_matrix is None:
            self.colour_matrix = np.full(
                shape=(len(self.data), len(self.data[0])), 
                fill_value=Colours.DEFAULT, 
                dtype=Colours
            )
        else:
            self.colour_matrix = colour_matrix
        
        assert len(set(len(row) for row in self.data)) == 1,\
            "`data` is of inconsistent shape. "\
            "Not all rows have the same length"
        assert (len(self.data) == len(self.colour_matrix)) and\
            (len(self.data[0]) == len(self.colour_matrix[0])),\
            "Data and Colour matrix do not have the same shapes. "\
            f"`data` -> {data.shape}, `colour_matrix` -> {colour_matrix.shape}"

    def shape(self)-> tuple[int, int]:
        """
        Only returns the shape of the outer two layers, not its contents
        """
        try:
            return self.data.shape[:2]
        except AttributeError:
            try:
                return (len(self.data), len(self.data[0]))
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    def change_colour(self, cell: tuple[int, int], colour: Colours):
        try:
            self.colour_matrix[cell] = colour 
        except KeyError:
            raise KeyError(
                f"Tried accessing index {cell} in `self.data`,"
                f" which has a shape of {self.shape()}."
            )
        
    def print(self)-> None:
        print(self.__str__())

    def _determine_minimum_inner_cell_width(self)-> int:
        minimum_inner_cell_width = 0
        for row in self.data:
            for item in row:
                width = 0
                if type(item) == tuple:
                    width = max(len(str(element)) for element in item)
                else:
                    width = len(str(item))
                if width > minimum_inner_cell_width:
                    minimum_inner_cell_width = width
        return max(3, minimum_inner_cell_width)
    
    def _determine_minimum_inner_cell_height(self)-> int:
        minimum_inner_cell_height = 1
        for row in self.data:
            for item in row:
                height = 0
                if type(item) == tuple:
                    height = len(item)
                if height > minimum_inner_cell_height:
                    minimum_inner_cell_height = height
        return minimum_inner_cell_height

    def __getitem__(self, index: tuple[int, int])-> T:
        try:
            return self.data[index]
        except KeyError:
            try:
                return self.data[index[0]][index[1]]
            except KeyError:
                raise KeyError(
                    f"Tried accessing index {index} in `self.data`,"
                    f" which has a shape of {self.shape()}."
                )
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    def __str__(self)-> str:
        """
        Stringify ASCITable class.

        Indices will be printed at the top and on the left.
        Any cell containing tuples will
        """
        # general information
        inner_cell_width = self._determine_minimum_inner_cell_width() + 2
        inner_cell_height = self._determine_minimum_inner_cell_height()
        _, n_columns = self.shape()

        dividing_line = f"{('─' * inner_cell_width + '┼') * n_columns}"\
            f"{'─' * inner_cell_width}"

        # heading row
        result  = f"┌{dividing_line.replace('┼', '┬')}┐\n"
        row_data = [
            f"{' ' * (inner_cell_width // 2 - (len(str(i)) // 2) )}"
            f"{str(i)}"
            f"{' ' * (inner_cell_width // 2 - (len(str(i)) // 2) - 1)}"
            for i in ['x↓ →y'] + list(range(n_columns))
        ]
        result += f"│{''.join(
            f"{Colours.BOLD_GREY.value}{data}{Colours.DEFAULT.value}"
            f"{' ' * (inner_cell_width - len(data))}│" 
            for data in row_data
        )}\n"

        # content rows
        for i, row in enumerate(self.data):
            # dividing line
            result += f"├{dividing_line}┤\n"

            for j in range(inner_cell_height):

                if j == inner_cell_height // 2 - 1 or inner_cell_height == 1:
                    primer = f"{' ' * (
                        inner_cell_width // 2 - len(str(i)) + 1
                    )}"\
                        f"{str(i)}"\
                        f"{' ' * (inner_cell_width // 2 - len(str(i)) - 1)}"
                    result += f"│{Colours.BOLD_GREY.value}"\
                        f"{primer}"\
                        f"{Colours.DEFAULT.value}"\
                        f"{' ' * (inner_cell_width - len(primer))}"
                else:
                    result += f"│{' ' * inner_cell_width}"

                # contents
                row_data = []
                for item in row:
                    try:
                        row_data.append(
                            f"{' ' * (
                                inner_cell_width // 2 - (
                                    len(str(item[j])) // 2
                                )
                            )}"
                            f"{str(item[j])}"
                            f"{' ' * (
                                inner_cell_width // 2 - (
                                    len(str(item[j])) // 2
                                ) - 1
                            )}"
                        )
                    except IndexError:
                        row_data.append(f"{' ' * inner_cell_width}")
                result += f"│{''.join(
                    f"{self.colour_matrix[i,k].value}"
                    f"{data}"
                    f"{Colours.DEFAULT.value}"
                    f"{' ' * (inner_cell_width - len(data))}│" 
                    for k, data in enumerate(row_data)
                )}\n"

        # ending line
        result  += f"└{dividing_line.replace('┼', '┴')}┘\n"

        return result
