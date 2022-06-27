import logging.config

import pygame
from board import Board
import config
import copy

from screen import Screen

logging.config.dictConfig(config.DEFAULT_LOGGING)
logger = logging.getLogger(__name__)


class Game:
    def __init__(self, board_filename: str, rounds_to_simulate: int = 5) -> None:
        """Initialize the game

        Args:
            board_filename (str): File with initial board values.
            rounds_to_simulate (int, optional): How many rounds to simulate. Defaults to 5.
        """
        self.board = Board(board_filename)
        self.screen = Screen(config.SCREEN_SIZE_X, config.SCREEN_SIZE_Y)
        self.rounds_to_simulate = rounds_to_simulate

        self.round = 0

    def run(self) -> None:
        """Method for starting the simulation"""
        self.screen.output_board(self.board)
        for round in range(self.rounds_to_simulate):
            self.round = round
            self.board.values = self.simulate_next_round()
            self.screen.output_board(self.board)

    def simulate_next_round(self) -> Board:
        """Simulates a new generation

        Returns:
            Board: The board state after the simulation
        """
        logger.debug(f"Simulating round {self.round}")
        new_board = [[0] * self.board.size[0] for i in range(self.board.size[1])]
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
