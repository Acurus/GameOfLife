import pygame
from board import Board
import config


class Screen:
    def __init__(self, screensize_x: int, screensize_y: int) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screensize_x = screensize_x
        self.screensize_y = screensize_y

        self.screen = pygame.display.set_mode(
            (self.screensize_x, self.screensize_y), 0, 24
        )

    def output_board(self, board: Board) -> None:
        """Displays the board at it's current state"""

        block_size = self.screensize_x / board.size[1] * 2
        circle_size = block_size / board.size[1] > 2 or 2

        self.clock.tick(config.TICK)
        for row in range(board.size[0]):
            for column in range(board.size[1]):

                if board.state_of_cell(row, column):
                    colour = pygame.Color(config.ALIVE_COLOUR)
                elif (
                    config.DISPLAY_CELLS_CHECKED
                    and ((row, column)) in board.cells_to_check_next
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
