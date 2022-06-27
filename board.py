import logging
import logging.config
import config

logging.config.dictConfig(config.DEFAULT_LOGGING)
logger = logging.getLogger(__name__)


class Board:
    def __init__(self, boardfilename: str) -> None:
        """Initialize the Board

        Args:
            boardfilename (str): File with starting pattern.
        """
        self.boardfilename = boardfilename
        self.values = self._initialize()
        self.size = (len(self.values[0]), len(self.values))
        self.cells_to_check_next = self.cells_to_check_first_round()
        logger.info(f"Initialized board with size: {self.size}")

    def _initialize(self) -> list:
        """Builds the board values from provided file

        Returns:
            list: 2D list of board values
        """
        board_values = []
        if self.boardfilename:
            logger.debug(f"Initializing board from file: {self.boardfilename}")
            with open(self.boardfilename, "r") as f:
                for line in f:
                    row_values = [int(x) for x in line.strip()]
                    board_values.append(row_values)
            return board_values
        else:
            return None

    def state_of_cell(self, row: int, column: int) -> int:
        """Get the state of a cell at provided coordinates

        Args:
            row (int):
            column (int):

        Returns:
            int: Returns 0 or 1
        """
        if row > len(self.values[0]) or column > len(self.values[1]):
            logger.error("Row or Column out of bounds! row: {row}  column: {column}")
            raise IndexError(
                f"Row or Column out of bounds! row: {row}  column: {column}"
            )

        return self.values[row][column]

    def next_state_of_cell(self, cell: tuple) -> int:
        """Finds state of a cell for the next generation

        Args:
            cell (tuple): tuple of (row, column)

        Returns:
            int: Returns 0 or 1
        """

        neighbours = self._neighbours_of_cell(cell)
        neighbour_values = neighbours.values()
        cell_value = self.state_of_cell(cell[0], cell[1])

        if cell_value == 1 and (
            sum(neighbour_values) == 2 or sum(neighbour_values) == 3
        ):
            new_cell_value = 1
            self.cells_to_check_next.add(cell)
            self.cells_to_check_next.update(neighbours.keys())
        elif cell_value == 0 and sum(neighbour_values) == 3:
            new_cell_value = 1
            self.cells_to_check_next.add(cell)
            self.cells_to_check_next.update(neighbours.keys())

        else:
            new_cell_value = 0

        if new_cell_value != cell_value:
            self.cells_to_check_next.add(cell)
            self.cells_to_check_next.update(neighbours.keys())

        return new_cell_value

    def _neighbours_of_cell(self, cell: tuple) -> dict:
        """Returns the neighbours of a cell at given coordinates

        Args:
            cell (tuple): tuple of (row, column)

        Returns:
            dict: dict of neighbours. {(row, column):0}
        """
        neighbours = {}

        for row_addition in range(-1, 2):
            for column_addition in range(-1, 2):
                if not (row_addition == 0 and column_addition == 0):
                    if cell[1] + column_addition > self.size[1] - 1:
                        neighbour_column = column_addition - self.size[1]
                    elif cell[1] + column_addition < -1 * self.size[1]:
                        neighbour_column = column_addition
                    else:
                        neighbour_column = cell[1] + column_addition

                    if cell[0] + row_addition > self.size[0] - 1:
                        neighbour_row = row_addition - self.size[0]
                    elif cell[0] + row_addition < -1 * self.size[0]:
                        neighbour_row = row_addition
                    else:
                        neighbour_row = cell[0] + row_addition

                    neighbours[neighbour_row, neighbour_column] = self.state_of_cell(
                        neighbour_row, neighbour_column
                    )

        return neighbours

    def cells_to_check_first_round(self) -> set:
        """Generate cell tuples for initial check

        Returns:
            list: _description_
        """
        cells_to_check = set()
        for row in range(self.size[0]):
            for column in range(self.size[1]):
                cells_to_check.add((row, column))

        return cells_to_check
