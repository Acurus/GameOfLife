import logging
from logging.config import dictConfig
import config

from game import Game


def main():
    logger.info("Starting")
    game = Game(config.BOARD_FILENAME, config.ROUNDS_TO_SIMULATE)
    game.run()
    logger.info("Finished")
    # input("Press enter to exit")


if __name__ == "__main__":
    dictConfig(config.DEFAULT_LOGGING)
    logger = logging.getLogger(__name__)
    main()
