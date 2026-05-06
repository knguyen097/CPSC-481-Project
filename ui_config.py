"""UI constants for the Connect 4 Pygame interface.

This file keeps colors, sizes, and layout values out of the main game
controller so they are easier to find and change later.
"""

from connect4 import ROWS, COLS

# Board and window sizing.
CELL_SIZE = 90
BOARD_TOP = 170
WIDTH = COLS * CELL_SIZE
HEIGHT = BOARD_TOP + ROWS * CELL_SIZE + 30
RADIUS = CELL_SIZE // 2 - 8

FPS = 60

# Color constants used throughout the interface.
BACKGROUND = (245, 247, 250)
BOARD_BLUE = (30, 95, 210)
EMPTY_SLOT = (235, 235, 235)
PLAYER_RED = (220, 45, 55)
AI_YELLOW = (245, 205, 55)
TEXT_DARK = (30, 30, 30)
BUTTON = (40, 90, 180)
BUTTON_HOVER = (65, 120, 220)
BUTTON_TEXT = (255, 255, 255)
WIN_OUTLINE = (255, 255, 255)
WHITE = (255, 255, 255)

# Transparent colors used for the player's move preview.
PREVIEW_RED = (220, 45, 55, 95)
PREVIEW_OUTLINE = (255, 255, 255, 190)