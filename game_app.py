"""Main game controller for the Connect 4 Pygame app.

This file owns the Pygame window, game state, event handling, turn changes,
pause behavior, restart behavior, and AI turn timing.
"""

import pygame

from ai import choose_move
from connect4 import Connect4, EMPTY, PLAYER, AI_PLAYER
from renderer import Renderer
from ui_config import FPS, HEIGHT, WIDTH


class GameApp:
    """Control the Connect 4 application from startup to shutdown."""

    def __init__(self):
        """Set up Pygame, the display, buttons, renderer, and starting game data."""
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Connect 4 - AI with Alpha-Beta Pruning")

        self.clock = pygame.time.Clock()
        self.renderer = Renderer(self.screen)
        self.stats = self.create_stats()
        self.data = self.reset_game()
        self.running = True

        self.create_buttons()

    def create_buttons(self):
        """Create all button rectangles used by menus and game-over screens."""
        button_width = 190
        button_height = 58
        start_y = 240

        # Difficulty buttons shown on the main menu.
        self.difficulty_buttons = {
            "easy": pygame.Rect(
                (WIDTH - button_width) // 2,
                start_y,
                button_width,
                button_height,
            ),
            "medium": pygame.Rect(
                (WIDTH - button_width) // 2,
                start_y + 80,
                button_width,
                button_height,
            ),
            "hard": pygame.Rect(
                (WIDTH - button_width) // 2,
                start_y + 160,
                button_width,
                button_height,
            ),
        }

        # Buttons shown when the game ends.
        self.restart_button = pygame.Rect(WIDTH // 2 - 210, HEIGHT // 2 + 55, 180, 60)
        self.menu_button = pygame.Rect(WIDTH // 2 + 30, HEIGHT // 2 + 55, 180, 60)

        # Buttons shown in the pause menu.
        self.resume_button = pygame.Rect(WIDTH // 2 - 210, HEIGHT // 2 - 35, 180, 60)
        self.pause_menu_button = pygame.Rect(WIDTH // 2 + 30, HEIGHT // 2 - 35, 180, 60)
        self.exit_button = pygame.Rect(WIDTH // 2 - 90, HEIGHT // 2 + 45, 180, 60)

    def reset_game(self):
        """Create a fresh game data dictionary.

        The dictionary stores the current game object and UI state.
        This keeps related game state grouped in one place.
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
    def create_stats(self):
        """Create win/loss/draw stats for the current play session."""
        return {
        "player_wins": 0,
        "ai_wins": 0,
        "draws": 0,
    }

    def run(self):
        """Run the main Pygame loop."""
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.handle_ai_turn()
            self.draw()
            pygame.display.flip()

        pygame.quit()

    def handle_events(self):
        """Handle all keyboard, mouse, and quit events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)

    def handle_keydown(self, event):
        """Handle pause and resume keyboard shortcuts."""
        if self.data["state"] == "playing" and event.key in (pygame.K_p, pygame.K_ESCAPE):
            self.data["state"] = "paused"
            self.data["message"] = "Game paused"

        elif self.data["state"] == "paused" and event.key in (pygame.K_p, pygame.K_ESCAPE):
            self.resume_game()

    def handle_mouse_click(self, mouse_pos):
        """Send mouse clicks to the correct handler based on the current state."""
        if self.data["state"] == "menu":
            self.handle_menu_click(mouse_pos)

        elif self.data["state"] == "playing" and self.data["turn"] == PLAYER:
            self.handle_player_click(mouse_pos)

        elif self.data["state"] == "paused":
            self.handle_pause_click(mouse_pos)

        elif self.data["state"] == "game_over":
            self.handle_game_over_click(mouse_pos)

    def handle_menu_click(self, mouse_pos):
        """Start a new game when the player chooses a difficulty."""
        for difficulty, rect in self.difficulty_buttons.items():
            if rect.collidepoint(mouse_pos):
                self.start_new_game(difficulty)
                return

    def handle_player_click(self, mouse_pos):
        """Handle the human player's board click."""
        col = self.renderer.get_column_from_mouse(mouse_pos)

        if col is None:
            return

        if self.data["game"].drop_piece(col, PLAYER):
            self.finish_turn()
        else:
            self.data["message"] = "That column is full. Choose another one."

    def handle_pause_click(self, mouse_pos):
        """Handle resume, main menu, and exit clicks from the pause menu."""
        if self.resume_button.collidepoint(mouse_pos):
            self.resume_game()

        elif self.pause_menu_button.collidepoint(mouse_pos):
            self.data = self.reset_game()

        elif self.exit_button.collidepoint(mouse_pos):
            self.running = False

    def handle_game_over_click(self, mouse_pos):
        """Handle restart and main menu clicks after a game ends."""
        if self.restart_button.collidepoint(mouse_pos):
            self.restart_same_difficulty()

        elif self.menu_button.collidepoint(mouse_pos):
            self.data = self.reset_game()

    def start_new_game(self, difficulty):
        """Start a fresh game with the selected difficulty."""
        self.data = self.reset_game()
        self.data["difficulty"] = difficulty
        self.data["state"] = "playing"
        self.data["message"] = "Your turn - click a column"

    def restart_same_difficulty(self):
        """Restart the board while keeping the player's selected difficulty."""
        difficulty = self.data["difficulty"]
        self.start_new_game(difficulty)

    def resume_game(self):
        """Resume gameplay from the pause menu."""
        self.data["state"] = "playing"

        if self.data["turn"] == PLAYER:
            self.data["message"] = "Your turn - click a column"
        else:
            self.data["message"] = "AI is thinking..."
            self.data["ai_move_time"] = pygame.time.get_ticks() + 400

    def record_result(self, winner):
        """Update the win tracker after a game ends."""
        if winner == PLAYER:
            self.stats["player_wins"] += 1

        elif winner == AI_PLAYER:
            self.stats["ai_wins"] += 1

        else:
            self.stats["draws"] += 1
      
      
    def create_stats(self):
        """Create win/loss/draw stats for the current play session."""
        return {
            "player_wins": 0,
            "ai_wins": 0,
            "draws": 0,
        }      
        
    def finish_turn(self):
        """Handle what happens after a player or AI finishes a move.

        This checks for a win, checks for a draw, and switches turns if the
        game is still active.
        """
        game = self.data["game"]
        winner = game.check_win()

        if winner != EMPTY:
            self.record_result(winner)
            
            self.data["winner"] = winner
            self.data["winning_cells"] = game.winning_cells()
            self.data["state"] = "game_over"

            if winner == PLAYER:
                self.data["message"] = "You Win!"
            else:
                self.data["message"] = "AI Wins!"

            return

        if game.is_full():
            self.record_result(EMPTY)
            
            self.data["state"] = "game_over"
            self.data["message"] = "Draw game!"
            return

        # Switch turns after a successful move.
        if self.data["turn"] == PLAYER:
            self.data["turn"] = AI_PLAYER
            self.data["message"] = "AI is thinking..."

            # Add a small delay so the AI move feels more natural.
            self.data["ai_move_time"] = pygame.time.get_ticks() + 400
        else:
            self.data["turn"] = PLAYER
            self.data["message"] = "Your turn - click a column"

    def handle_ai_turn(self):
        """Run the AI turn after the short thinking delay."""
        if self.data["state"] != "playing":
            return

        if self.data["turn"] != AI_PLAYER:
            return

        if pygame.time.get_ticks() < self.data["ai_move_time"]:
            return

        ai_col = choose_move(
            self.data["game"],
            AI_PLAYER,
            self.data["difficulty"],
        )

        if ai_col is not None:
            self.data["game"].drop_piece(ai_col, AI_PLAYER)

        self.finish_turn()

    def draw(self):
        """Draw the correct screen based on the current game state."""
        if self.data["state"] == "menu":
            self.renderer.draw_menu(self.data, self.difficulty_buttons)

        elif self.data["state"] == "paused":
            self.renderer.draw_game(
                self.data, 
                self.restart_button, 
                self.menu_button, 
                self.stats,
                )
            self.renderer.draw_pause_menu(
                self.resume_button,
                self.pause_menu_button,
                self.exit_button,
            )

        else:
            self.renderer.draw_game(
                self.data, 
                self.restart_button, 
                self.menu_button, 
                self.stats,
            )