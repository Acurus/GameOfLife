import logging
import logging.config
import sys
from turtle import screensize
import pygame
from time import sleep
import copy


def setup_logger():
    DEFAULT_LOGGING = {
        "version": 1,
        "formatters": {
            "standard": {
                "format": "%(asctime)s %(levelname)s: %(message)s",
                "datefmt": "%Y-%m-%d - %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "level": "INFO",
                "stream": sys.stdout,
            },
            "file": {
                "class": "logging.FileHandler",
                "formatter": "standard",
                "level": "DEBUG",
                "filename": "logfile.log",
                "mode": "w",
            },
        },
        "loggers": {
            __name__: {
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(DEFAULT_LOGGING)
    logger = logging.getLogger(__name__)
    return logger


class Board:
    def __init__(self, boardfilename: str = None):
        self.boardfilename = boardfilename
        self.values = self._initialize()
        self.size = (len(self.values[0]), len(self.values))
        logger.info(f"Initialized board with size: {self.size}")

    def _initialize(self):
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

    def state_of_cell(self, row: int, column: int):
        return self.values[row][column]

    def next_state_of_cell(self, cell: tuple):

        neighbour_values = self._neighbours_of_cell(cell)
        cell_value = self.state_of_cell(cell[0], cell[1])
        if cell_value == 1 and (
            sum(neighbour_values) == 2 or sum(neighbour_values) == 3
        ):
            return 1
        elif cell_value == 0 and sum(neighbour_values) == 3:
            return 1
        else:
            return 0

    def load_from_file(self):
        pass

    def _neighbours_of_cell(self, cell: tuple) -> list:
        neighbours = []
        for row_addition in range(-1, 2):
            for column_addition in range(-1, 2):
                if not (row_addition == 0 and column_addition == 0):
                    if cell[1] + column_addition > self.size[1] - 1:
                        neighbour_column = column_addition - self.size[1]
                    else:
                        neighbour_column = cell[1] + column_addition

                    if cell[0] + row_addition > self.size[0] - 1:
                        neighbour_row = row_addition - self.size[0]
                    else:
                        neighbour_row = cell[0] + row_addition

                    neighbours.append(
                        self.state_of_cell(neighbour_row, neighbour_column)
                    )
        return neighbours


class Game:
    def __init__(self, board_filename: str = None, rounds_to_simulate: int = 5):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screensize_x = 600
        self.screensize_y = 600
        self.screen = pygame.display.set_mode(
            (self.screensize_x, self.screensize_y), 0, 24
        )
        self.rounds_to_simulate = rounds_to_simulate
        self.board = Board(board_filename)
        self.round = 0

    def run(self):
        self.output_board()
        for round in range(self.rounds_to_simulate):
            self.round = round
            self.board.values = self.simulate_next_round()
            self.output_board()
        input("Press enter to exit")

    def simulate_next_round(self):
        logger.debug(f"Simulating round {self.round}")
        new_board = [[0] * self.board.size[0] for i in range(self.board.size[1])]
        for row in range(self.board.size[0]):
            for column in range(self.board.size[1]):
                if row == 3 and column == 4:
                    print("Debug!")
                new_board[row][column] = self.board.next_state_of_cell((row, column))
                logger.debug(
                    f"row{row} column{column} changed: { self.board.values[row][column] != new_board[row][column]}"
                )
        logger.info(f"simulated round: {self.round}")
        return new_board

    def output_board(self):
        block_size = self.screensize_x / game.board.size[1] * 2
        circle_size = block_size / game.board.size[1] > 2 or 2
        alive_colour = pygame.Color(0, 255, 0)
        dead_colour = pygame.Color(0, 0, 0)

        self.clock.tick(30)
        for i in range(self.board.size[0]):
            for j in range(self.board.size[1]):
                if self.board.state_of_cell(i, j):
                    colour = alive_colour
                else:
                    colour = dead_colour
                center_point = (
                    (j * (block_size / 2)),
                    (i * (block_size / 2)),
                )
                pygame.draw.circle(self.screen, colour, center_point, circle_size, 0)
        pygame.display.flip()


if __name__ == "__main__":
    logger = setup_logger()
    game = Game(r"board60x60.txt", 300)
    game.run()
