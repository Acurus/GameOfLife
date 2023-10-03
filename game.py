import logging.config

import pygame
from board import Board
import config
import copy

logging.config.dictConfig(config.DEFAULT_LOGGING)
logger = logging.getLogger(__name__)


class Game:
    def __init__(self, board_filename: str, rounds_to_simulate: int = 5) -> None:
        """Initialize the game

        Args:
            board_filename (str): File with initial board values.
            rounds_to_simulate (int, optional): How many rounds to simulate. Defaults to 5.
        """
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screensize_x = config.SCREEN_SIZE_X
        self.screensize_y = config.SCREEN_SIZE_Y
        self.screen = pygame.display.set_mode(
            (self.screensize_x, self.screensize_y), 0, 24
        )
        self.rounds_to_simulate = rounds_to_simulate
        self.board = Board(board_filename)
        self.round = 0

    def run(self) -> None:
        """Method for starting the simulation"""
        self.output_board()
        for round in range(self.rounds_to_simulate):
            self.round = round
            self.board.values = self.simulate_next_round()
            self.output_board()

    def simulate_next_round(self) -> Board:
        """Simulates a new generation

        Returns:
            Board: The board state after the simulation
        """
        logger.debug(f"Simulating round {self.round}")
        new_board = [[0] * self.board.number_of_columns for i in range(self.board.number_of_rows)]
        cells_to_check = copy.deepcopy(self.board.cells_to_check_next)
        logger.info(f"Checking {len(cells_to_check)} cells")
        self.board.cells_to_check_next = set()

        for cell in cells_to_check:
            row = cell[0]
            column = cell[1]
            new_board[row][column] = self.board.next_state_of_cell((row, column))

        cells_to_check = []
        logger.info(f"simulated round: {self.round}")
        return new_board

    def output_board(self) -> None:
        """Displays the board at it's current state"""
        largest_side = max([self.board.number_of_rows, self.board.number_of_columns])
        block_size = self.screensize_x / largest_side * 2
        circle_size = block_size / largest_side > 2 or 2

        self.clock.tick(config.TICK)
        for row in range(self.board.number_of_rows):
            for column in range(self.board.number_of_columns):
                if self.board.state_of_cell(row, column):
                    colour = pygame.Color(config.ALIVE_COLOUR)
                elif (
                    config.DISPLAY_CELLS_CHECKED
                    and ((row, column)) in self.board.cells_to_check_next
                ):
                    colour = pygame.Color(config.DISPLAY_CELLS_CHECKED_COLOUR)
                else:
                    colour = pygame.Color(config.DEAD_COLOR)
                center_point = (
                    (column * (block_size / 2)),
                    (row * (block_size / 2)),
                )
                pygame.draw.circle(self.screen, colour, center_point, circle_size, 0)
        pygame.display.flip()
