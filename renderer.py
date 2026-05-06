"""Drawing helpers for the Connect 4 Pygame interface.

The renderer is responsible only for visuals. It does not decide turns,
run the AI, or change the board. This keeps the game controller cleaner.
"""

import pygame

from connect4 import ROWS, COLS, PLAYER, AI_PLAYER
from ui_config import (
    AI_YELLOW,
    BACKGROUND,
    BOARD_BLUE,
    BOARD_TOP,
    BUTTON,
    BUTTON_HOVER,
    BUTTON_TEXT,
    CELL_SIZE,
    EMPTY_SLOT,
    HEIGHT,
    PLAYER_RED,
    PREVIEW_OUTLINE,
    PREVIEW_RED,
    RADIUS,
    TEXT_DARK,
    WHITE,
    WIDTH,
    WIN_OUTLINE,
)


class Renderer:
    """Draw all screens, buttons, text, board pieces, and overlays."""

    def __init__(self, screen):
        """Store the Pygame screen used for drawing."""
        self.screen = screen

    def make_font(self, size, bold=False):
        """Create a font object with a consistent font family."""
        return pygame.font.SysFont("arial", size, bold=bold)

    def draw_text(self, text, size, x, y, color=TEXT_DARK, bold=False, center=True):
        """Draw text on the screen.

        The center option allows the same function to be used for centered
        titles and left-aligned labels.
        """
        font = self.make_font(size, bold)
        surface = font.render(text, True, color)
        rect = surface.get_rect()

        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)

        self.screen.blit(surface, rect)

    def draw_button(self, rect, text):
        """Draw a clickable button with a hover effect."""
        mouse_pos = pygame.mouse.get_pos()
        color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON

        pygame.draw.rect(self.screen, color, rect, border_radius=12)
        self.draw_text(text, 24, rect.centerx, rect.centery, BUTTON_TEXT, bold=True)

    def draw_board(self, game, winning_cells=None):
        """Draw the Connect 4 board and all placed pieces."""
        if winning_cells is None:
            winning_cells = []

        pygame.draw.rect(
            self.screen,
            BOARD_BLUE,
            (0, BOARD_TOP, WIDTH, ROWS * CELL_SIZE),
        )

        for row in range(ROWS):
            for col in range(COLS):
                x = col * CELL_SIZE + CELL_SIZE // 2
                y = BOARD_TOP + row * CELL_SIZE + CELL_SIZE // 2
                value = game.board[row][col]

                if value == PLAYER:
                    piece_color = PLAYER_RED
                elif value == AI_PLAYER:
                    piece_color = AI_YELLOW
                else:
                    piece_color = EMPTY_SLOT

                pygame.draw.circle(self.screen, piece_color, (x, y), RADIUS)

                # Highlight the four pieces that caused the win.
                if (row, col) in winning_cells:
                    pygame.draw.circle(self.screen, WIN_OUTLINE, (x, y), RADIUS, 5)

    def get_column_from_mouse(self, pos):
        """Convert the mouse position into a board column.

        Returns None if the mouse is above the board or outside the board width.
        """
        x, y = pos

        if y < BOARD_TOP:
            return None

        col = x // CELL_SIZE

        if 0 <= col < COLS:
            return col

        return None

    def draw_menu(self, data, buttons):
        """Draw the main menu and difficulty buttons."""
        self.screen.fill(BACKGROUND)
        self.draw_text("Connect 4", 52, WIDTH // 2, 65, TEXT_DARK, bold=True)
        self.draw_text("Can you beat AI?", 24, WIDTH // 2, 115)

        for difficulty, rect in buttons.items():
            self.draw_button(rect, difficulty.capitalize())

        self.draw_text(
            "Easy = random moves | Medium/Hard = smarter AI",
            20,
            WIDTH // 2,
            HEIGHT - 60,
        )

    def draw_stats(self, stats):
        """Draw the current session win/loss stats."""
        if stats is None:
            return

        player_wins = stats["player_wins"]
        ai_wins = stats["ai_wins"]
        draws = stats["draws"]
        total_games = player_wins + ai_wins + draws

        if total_games == 0:
            player_rate = 0
            ai_rate = 0
        else:
            player_rate = (player_wins / total_games) * 100
            ai_rate = (ai_wins / total_games) * 100

        stats_text = (
            f"You: {player_wins} wins ({player_rate:.0f}%)  |  "
            f"AI: {ai_wins} wins ({ai_rate:.0f}%)  |  "
            f"Draws: {draws}"
        )

        self.draw_text(
            stats_text,
            17,
            WIDTH // 2,
            140,
            TEXT_DARK,
        )

    def draw_game(self, data, restart_button, menu_button, stats=None):
        """Draw the gameplay screen.

        This includes the title, current message, board, piece preview,
        and game-over overlay when the game ends.
        """
        self.screen.fill(BACKGROUND)

        self.draw_text("Connect 4", 36, WIDTH // 2, 35, TEXT_DARK, bold=True)
        self.draw_text(data["message"], 26, WIDTH // 2, 82, TEXT_DARK)
        
        self.draw_text(
            f"Difficulty: {data['difficulty'].capitalize()}",
            20,
            WIDTH // 2,
            118,
            TEXT_DARK,
        )
        
        self.draw_stats(stats)
        self.draw_text("Press P or Esc to pause", 18, WIDTH // 2, HEIGHT - 15, TEXT_DARK)

        self.draw_board(data["game"], data["winning_cells"])
        self.draw_piece_preview(data)

        if data["state"] == "game_over":
            # Light overlay helps separate the game-over message from the board.
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 150))
            self.screen.blit(overlay, (0, 0))

            panel_rect = pygame.Rect(WIDTH // 2 - 250, HEIGHT // 2 - 70, 500, 210)
            pygame.draw.rect(self.screen, WHITE, panel_rect, border_radius=20)

            self.draw_text(data["message"], 44, WIDTH // 2, HEIGHT // 2, TEXT_DARK, bold=True)
            self.draw_button(restart_button, "Play Again")
            self.draw_button(menu_button, "Main Menu")

    def draw_piece_preview(self, data):
        """Draw a transparent preview of where the player's piece will land.

        This only appears during the player's turn while the game is active.
        """
        if data["state"] != "playing":
            return

        if data["turn"] != PLAYER:
            return

        mouse_pos = pygame.mouse.get_pos()
        col = self.get_column_from_mouse(mouse_pos)
        row = data["game"].get_drop_row(col)

        if row is None:
            return

        x = col * CELL_SIZE + CELL_SIZE // 2
        y = BOARD_TOP + row * CELL_SIZE + CELL_SIZE // 2

        # Use a transparent surface so the preview does not look like a real piece.
        preview_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        pygame.draw.circle(
            preview_surface,
            PREVIEW_RED,
            (x, y),
            RADIUS,
        )

        pygame.draw.circle(
            preview_surface,
            PREVIEW_OUTLINE,
            (x, y),
            RADIUS,
            4,
        )

        self.screen.blit(preview_surface, (0, 0))

    def draw_pause_menu(self, resume_button, pause_menu_button, exit_button):
        """Draw the pause overlay and pause menu buttons."""
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        self.screen.blit(overlay, (0, 0))

        self.draw_text("Paused", 52, WIDTH // 2, HEIGHT // 2 - 100, WHITE, bold=True)

        self.draw_button(resume_button, "Resume")
        self.draw_button(pause_menu_button, "Main Menu")
        self.draw_button(exit_button, "Exit Game")