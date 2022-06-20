import logging.config

import pygame
from board import Board
import config

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
        new_board = [[0] * self.board.size[0] for i in range(self.board.size[1])]
        for row in range(self.board.size[0]):
            for column in range(self.board.size[1]):
                new_board[row][column] = self.board.next_state_of_cell((row, column))
                logger.debug(
                    f"row{row} column{column} changed: { self.board.values[row][column] != new_board[row][column]}"
                )
        logger.info(f"simulated round: {self.round}")
        return new_board

    def output_board(self) -> None:
        """Displays the board at it's current state"""
        block_size = self.screensize_x / self.board.size[1] * 2
        circle_size = block_size / self.board.size[1] > 2 or 2

        self.clock.tick(config.TICK)
        for i in range(self.board.size[0]):
            for j in range(self.board.size[1]):
                if self.board.state_of_cell(i, j):
                    colour = pygame.Color(config.ALIVE_COLOUR)
                else:
                    colour = pygame.Color(config.DEAD_COLOR)
                center_point = (
                    (j * (block_size / 2)),
                    (i * (block_size / 2)),
                )
                pygame.draw.circle(self.screen, colour, center_point, circle_size, 0)
        pygame.display.flip()
