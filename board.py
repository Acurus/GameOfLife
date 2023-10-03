import logging
import logging.config
import config
from PIL import Image
from pathlib import Path

logging.config.dictConfig(config.DEFAULT_LOGGING)
logger = logging.getLogger(__name__)


class Board:
    def __init__(self, boardfilename: Path) -> None:
        """Initialize the Board

        Args:
            boardfilename (str): File with starting pattern.
        """
        self.boardfilename = boardfilename
        self.values = self._initialize()
        self.number_of_rows = len(self.values)
        self.number_of_columns = len(self.values[0])
        self.cells_to_check_next = self.cells_to_check_first_round()
        logger.info(f"Initialized board with size: {self.number_of_rows} x {self.number_of_columns}")

    def _initialize(self) -> list:
        """Builds the board values from provided file

        Returns:
            list: 2D list of board values
        """

        if self.boardfilename.suffix == ".txt":
            return self._board_from_txt()

        elif self.boardfilename.suffix == ".tif":
            return self._board_from_tif()

        else:
            logger.error(f"Filetype not supported")
            return None

    def state_of_cell(self, row: int, column: int) -> int:
        """Get the state of a cell at provided coordinates

        Args:
            row (int):
            column (int):

        Returns:
            int: Returns 0 or 1
        """
        if row >= self.number_of_rows or column >= self.number_of_columns:
            logger.error(
                "Row or Column out of bounds! row: {row}  column: {column}")
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
                    if cell[1] + column_addition > self.number_of_columns - 1:
                        neighbour_column = column_addition - self.number_of_columns
                    elif cell[1] + column_addition < -1 * self.number_of_columns:
                        neighbour_column = column_addition
                    else:
                        neighbour_column = cell[1] + column_addition

                    if cell[0] + row_addition > self.number_of_rows - 1:
                        neighbour_row = row_addition - self.number_of_rows
                    elif cell[0] + row_addition < -1 * self.number_of_rows:
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
        for row in range(self.number_of_rows):
            for column in range(self.number_of_columns):
                cells_to_check.add((row, column))

        return cells_to_check

    def _board_from_txt(self):
        board_values = []
        logger.debug(
            f"Initializing board from text file: {self.boardfilename}")
        with open(self.boardfilename, "r") as f:
            for line in f:
                row_values = [int(x) for x in line.strip()]
                board_values.append(row_values)
        return board_values

    def _board_from_tif(self):
        board_values = []
        logger.debug(
            f"Initializing board from tiff file: {self.boardfilename}")
        im = Image.open(self.boardfilename).convert("L")
        rows, columns = im.size
        pixels = list(im.getdata())
        counter = 0
        for row in range(rows):
            board_values.append([])
            for _ in range(columns):
                if pixels[counter] == 255:
                    board_values[row].append(0)
                else:
                    board_values[row].append(1)
                counter += 1
        return board_values
