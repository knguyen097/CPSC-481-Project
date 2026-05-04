#!/usr/bin/env python3
"""Pygame runner for Connect 4 with an AI opponent.

This file handles the visual interface, user input, game states,
buttons, pause menu, and AI turns.

The actual Connect 4 rules are stored in connect4.py.
The AI decision-making is stored in ai.py.
"""

import pygame
from ai import choose_move
from connect4 import Connect4, ROWS, COLS, EMPTY, PLAYER, AI_PLAYER

pygame.init()

# Board and window sizing.
CELL_SIZE = 90
BOARD_TOP = 150
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

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4 - AI with Alpha-Beta Pruning")
clock = pygame.time.Clock()

def make_font(size, bold=False):
    """Create a font object with a consistent font family."""
    return pygame.font.SysFont("arial", size, bold=bold)

def draw_text(text, size, x, y, color=TEXT_DARK, bold=False, center=True):
    """Draw text on the screen.

    The center option allows the same function to be used for centered
    titles and left-aligned labels.
    """
    font = make_font(size, bold)
    surface = font.render(text, True, color)
    rect = surface.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    screen.blit(surface, rect)

def draw_button(rect, text):
    """Draw a clickable button with a hover effect."""
    mouse_pos = pygame.mouse.get_pos()
    color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON

    pygame.draw.rect(screen, color, rect, border_radius=12)
    draw_text(text, 24, rect.centerx, rect.centery, BUTTON_TEXT, bold=True)

def draw_board(game, winning_cells=None):
    """Draw the Connect 4 board and all placed pieces."""
    if winning_cells is None:
        winning_cells = []

    pygame.draw.rect(screen, BOARD_BLUE, (0, BOARD_TOP, WIDTH, ROWS * CELL_SIZE))

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

            pygame.draw.circle(screen, piece_color, (x, y), RADIUS)

            # Highlight the four pieces that caused the win.
            if (row, col) in winning_cells:
                pygame.draw.circle(screen, WIN_OUTLINE, (x, y), RADIUS, 5)

def get_column_from_mouse(pos):
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

def reset_game():
    """Create a fresh game data dictionary.

    The dictionary stores the current game object and UI state.
    This keeps the main loop simpler because all game state is grouped
    in one place.
    """
    return {
        "game": Connect4(),
        "turn": PLAYER,
        "difficulty": "medium",
        "state": "menu",
        "message": "Choose a difficulty",
        "winner": EMPTY,
        "winning_cells": [],
        "ai_move_time": 0,
    }

def finish_turn(data):
    """Handle what happens after a player or AI finishes a move.

    This checks for a win, checks for a draw, and switches turns if the
    game is still active.
    """
    game = data["game"]
    winner = game.check_win()

    if winner != EMPTY:
        data["winner"] = winner
        data["winning_cells"] = game.winning_cells()
        data["state"] = "game_over"

        if winner == PLAYER:
            data["message"] = "You Win!"
        else:
            data["message"] = "AI Wins!"

        return

    if game.is_full():
        data["state"] = "game_over"
        data["message"] = "Draw game!"
        return

    # Switch turns after a successful move.
    if data["turn"] == PLAYER:
        data["turn"] = AI_PLAYER
        data["message"] = "AI is thinking..."

        # Add a small delay so the AI move feels more natural.
        data["ai_move_time"] = pygame.time.get_ticks() + 400
    else:
        data["turn"] = PLAYER
        data["message"] = "Your turn - click a column"

def draw_menu(data, buttons):
    """Draw the main menu and difficulty buttons."""
    screen.fill(BACKGROUND)
    draw_text("Connect 4", 52, WIDTH // 2, 65, TEXT_DARK, bold=True)
    draw_text("Can you beat AI?", 24, WIDTH // 2, 115)

    for difficulty, rect in buttons.items():
        draw_button(rect, difficulty.capitalize())

    draw_text(
        "Easy = random moves | Medium/Hard = smarter AI",
        20,
        WIDTH // 2,
        HEIGHT - 60
    )

def draw_game(data, restart_button, menu_button):
    """Draw the gameplay screen.

    This includes the title, current message, board, piece preview,
    and game-over overlay when the game ends.
    """
    screen.fill(BACKGROUND)

    draw_text("Connect 4", 36, WIDTH // 2, 35, TEXT_DARK, bold=True)
    draw_text(data["message"], 26, WIDTH // 2, 82, TEXT_DARK)
    draw_text(
        f"Difficulty: {data['difficulty'].capitalize()}",
        20,
        WIDTH // 2,
        118,
        TEXT_DARK
    )
    draw_text("Press P or Esc to pause", 18, WIDTH // 2, HEIGHT - 15, TEXT_DARK)

    draw_board(data["game"], data["winning_cells"])
    draw_piece_preview(data)

    if data["state"] == "game_over":
        # Light overlay helps separate the game-over message from the board.
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 150))
        screen.blit(overlay, (0, 0))

        panel_rect = pygame.Rect(WIDTH // 2 - 250, HEIGHT // 2 - 70, 500, 210)
        pygame.draw.rect(screen, WHITE, panel_rect, border_radius=20)

        draw_text(data["message"], 44, WIDTH // 2, HEIGHT // 2, TEXT_DARK, bold=True)
        draw_button(restart_button, "Play Again")
        draw_button(menu_button, "Main Menu")

def draw_piece_preview(data):
    """Draw a transparent preview of where the player's piece will land.

    This only appears during the player's turn while the game is active.
    """
    if data["state"] != "playing":
        return

    if data["turn"] != PLAYER:
        return

    mouse_pos = pygame.mouse.get_pos()
    col = get_column_from_mouse(mouse_pos)
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
        RADIUS
    )

    pygame.draw.circle(
        preview_surface,
        PREVIEW_OUTLINE,
        (x, y),
        RADIUS,
        4
    )

    screen.blit(preview_surface, (0, 0))

def draw_pause_menu(resume_button, pause_menu_button, exit_button):
    """Draw the pause overlay and pause menu buttons."""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    screen.blit(overlay, (0, 0))

    draw_text("Paused", 52, WIDTH // 2, HEIGHT // 2 - 170, WHITE, bold=True)

    draw_button(resume_button, "Resume")
    draw_button(pause_menu_button, "Main Menu")
    draw_button(exit_button, "Exit Game")

def main():
    """Run the main Pygame loop."""
    data = reset_game()

    button_width = 190
    button_height = 58
    start_y = 240

    # Difficulty buttons shown on the main menu.
    difficulty_buttons = {
        "easy": pygame.Rect(
            (WIDTH - button_width) // 2,
            start_y,
            button_width,
            button_height
        ),
        "medium": pygame.Rect(
            (WIDTH - button_width) // 2,
            start_y + 80,
            button_width,
            button_height
        ),
        "hard": pygame.Rect(
            (WIDTH - button_width) // 2,
            start_y + 160,
            button_width,
            button_height
        ),
    }

    # Buttons shown when the game ends.
    restart_button = pygame.Rect(WIDTH // 2 - 210, HEIGHT // 2 + 55, 180, 60)
    menu_button = pygame.Rect(WIDTH // 2 + 30, HEIGHT // 2 + 55, 180, 60)

    # Buttons shown in the pause menu.
    resume_button = pygame.Rect(WIDTH // 2 - 210, HEIGHT // 2 - 35, 180, 60)
    pause_menu_button = pygame.Rect(WIDTH // 2 + 30, HEIGHT // 2 - 35, 180, 60)
    exit_button = pygame.Rect(WIDTH // 2 - 90, HEIGHT // 2 + 45, 180, 60)

    running = True

    while running:
        clock.tick(FPS)

        # Handle keyboard, mouse, and quit events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if data["state"] == "playing" and event.key in (
                    pygame.K_p,
                    pygame.K_ESCAPE
                ):
                    data["state"] = "paused"
                    data["message"] = "Game paused"

                elif data["state"] == "paused" and event.key in (
                    pygame.K_p,
                    pygame.K_ESCAPE
                ):
                    data["state"] = "playing"

                    if data["turn"] == PLAYER:
                        data["message"] = "Your turn - click a column"
                    else:
                        data["message"] = "AI is thinking..."
                        data["ai_move_time"] = pygame.time.get_ticks() + 400

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if data["state"] == "menu":
                    # Start a new game when the player chooses a difficulty.
                    for difficulty, rect in difficulty_buttons.items():
                        if rect.collidepoint(mouse_pos):
                            data = reset_game()
                            data["difficulty"] = difficulty
                            data["state"] = "playing"
                            data["message"] = "Your turn - click a column"

                elif data["state"] == "playing" and data["turn"] == PLAYER:
                    # Human player chooses a column by clicking on the board.
                    col = get_column_from_mouse(mouse_pos)

                    if col is not None:
                        if data["game"].drop_piece(col, PLAYER):
                            finish_turn(data)
                        else:
                            data["message"] = "That column is full. Choose another one."

                elif data["state"] == "paused":
                    if resume_button.collidepoint(mouse_pos):
                        data["state"] = "playing"

                        if data["turn"] == PLAYER:
                            data["message"] = "Your turn - click a column"
                        else:
                            data["message"] = "AI is thinking..."
                            data["ai_move_time"] = pygame.time.get_ticks() + 400

                    elif pause_menu_button.collidepoint(mouse_pos):
                        data = reset_game()

                    elif exit_button.collidepoint(mouse_pos):
                        running = False

                elif data["state"] == "game_over":
                    if restart_button.collidepoint(mouse_pos):
                        # Restart using the same difficulty the player selected.
                        difficulty = data["difficulty"]
                        data = reset_game()
                        data["difficulty"] = difficulty
                        data["state"] = "playing"
                        data["message"] = "Your turn - click a column"

                    elif menu_button.collidepoint(mouse_pos):
                        data = reset_game()

        # Run the AI turn after the short thinking delay.
        if data["state"] == "playing" and data["turn"] == AI_PLAYER:
            if pygame.time.get_ticks() >= data["ai_move_time"]:
                ai_col = choose_move(data["game"], AI_PLAYER, data["difficulty"])

                if ai_col is not None:
                    data["game"].drop_piece(ai_col, AI_PLAYER)

                finish_turn(data)

        # Draw the correct screen based on the current game state.
        if data["state"] == "menu":
            draw_menu(data, difficulty_buttons)

        elif data["state"] == "paused":
            draw_game(data, restart_button, menu_button)
            draw_pause_menu(resume_button, pause_menu_button, exit_button)

        else:
            draw_game(data, restart_button, menu_button)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()