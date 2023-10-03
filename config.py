import sys

BOARD_FILENAME = "boards/demultiplexer.txt"
LOG_FILENAME = "logfile.log"

ROUNDS_TO_SIMULATE = 500  # How many rounds to simulate

ALIVE_COLOUR = (0, 255, 0)  # Colour of alive cells in pygame screen
DEAD_COLOR = (0, 0, 0)  # Colour of dead cells in pygame screen
SCREEN_SIZE_X = 800  # Pygame screen
SCREEN_SIZE_Y = 800  # Pygame screen
TICK = 30  # Pygame clock tick
LOGGING_LEVEL = "INFO"
DISPLAY_CELLS_CHECKED = False
DISPLAY_CELLS_CHECKED_COLOUR = (0, 0, 255)
DEFAULT_LOGGING = {
    "version": 1,
    "formatters": {
        "standard": {
            "format": "%(name)s %(asctime)s %(levelname)s: %(message)s",
            "datefmt": "%Y-%m-%d - %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "WARNING",
            "stream": sys.stdout,
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "standard",
            "level": LOGGING_LEVEL,
            "filename": LOG_FILENAME,
            "mode": "w",
        },
    },
    "loggers": {
        "__main__": {
            "level": LOGGING_LEVEL,
            "handlers": ["console", "file"],
            "propagate": False,
        },
        "game": {
            "level": LOGGING_LEVEL,
            "handlers": ["console", "file"],
            "propagate": False,
        },
        "board": {
            "level": LOGGING_LEVEL,
            "handlers": ["console", "file"],
            "propagate": False,
        },
    },
}
