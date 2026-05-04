"""Core Connect 4 game logic.

This file does not depend on Pygame or terminal input.
It only manages the board, valid moves, piece placement, win checking,
and helper methods used by the AI and the Pygame interface.
"""

ROWS = 6
COLS = 7

EMPTY = 0
PLAYER = 1
AI_PLAYER = 2

class Connect4:
    """Represent the Connect 4 board and core game rules."""

    def __init__(self):
        """Create a new empty Connect 4 board."""
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

    def reset(self):
        """Clear the board and start a new game."""
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

    def copy(self):
        """Return a separate copy of the current game state.

        The AI uses copies of the board to simulate future moves without
        changing the real game currently being played.
        """
        new_game = Connect4()
        new_game.board = [row[:] for row in self.board]
        return new_game

    def valid_moves(self):
        """Return a list of columns that are not full."""
        return [col for col in range(COLS) if self.board[0][col] == EMPTY]

    def is_valid_move(self, col):
        """Return True if a piece can be dropped in the selected column."""
        if col is None:
            return False

        return 0 <= col < COLS and self.board[0][col] == EMPTY

    def get_drop_row(self, col):
        """Return the row where a piece would land in the selected column.

        This is useful for the preview feature because it lets the UI show
        where the player's piece will land before the player clicks.
        """
        if col is None:
            return None

        if not self.is_valid_move(col):
            return None

        # Start from the bottom row because Connect 4 pieces fall downward.
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][col] == EMPTY:
                return row

        return None

    def drop_piece(self, col, player):
        """Drop a piece into a column for the selected player.

        Returns:
            True if the move was successful.
            False if the column was invalid or already full.
        """
        if not self.is_valid_move(col):
            return False

        # Place the piece in the lowest available row of the column.
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][col] == EMPTY:
                self.board[row][col] = player
                return True

        return False

    def is_full(self):
        """Return True if the board has no available moves left."""
        return all(self.board[0][col] != EMPTY for col in range(COLS))

    def check_win(self):
        """Check whether either player has connected four pieces.

        Returns:
            EMPTY if there is no winner.
            PLAYER if the human player wins.
            AI_PLAYER if the AI wins.
        """
        for row in range(ROWS):
            for col in range(COLS):
                player = self.board[row][col]

                # Empty spaces cannot start a winning line.
                if player == EMPTY:
                    continue

                # Check horizontal line.
                if col <= COLS - 4 and all(
                    self.board[row][col + i] == player for i in range(4)
                ):
                    return player

                # Check vertical line.
                if row <= ROWS - 4 and all(
                    self.board[row + i][col] == player for i in range(4)
                ):
                    return player

                # Check diagonal line going down and to the right.
                if row <= ROWS - 4 and col <= COLS - 4 and all(
                    self.board[row + i][col + i] == player for i in range(4)
                ):
                    return player

                # Check diagonal line going up and to the right.
                if row >= 3 and col <= COLS - 4 and all(
                    self.board[row - i][col + i] == player for i in range(4)
                ):
                    return player

        return EMPTY

    def winning_cells(self):
        """Return the four board positions that form the winning line.

        The Pygame interface uses these cells to draw a highlight around
        the winning pieces after the game ends.
        """
        directions = [
            (0, 1),    # horizontal
            (1, 0),    # vertical
            (1, 1),    # diagonal down-right
            (-1, 1),   # diagonal up-right
        ]

        for row in range(ROWS):
            for col in range(COLS):
                player = self.board[row][col]

                if player == EMPTY:
                    continue

                for row_step, col_step in directions:
                    cells = []

                    # Build a possible group of four cells in the current direction.
                    for i in range(4):
                        next_row = row + row_step * i
                        next_col = col + col_step * i

                        if 0 <= next_row < ROWS and 0 <= next_col < COLS:
                            cells.append((next_row, next_col))

                    # If all four cells belong to the same player, this is the win.
                    if len(cells) == 4 and all(
                        self.board[r][c] == player for r, c in cells
                    ):
                        return cells

        return []

    def render(self):
        """Return a text version of the board for debugging.

        The Pygame version does not use this during normal gameplay,
        but it is useful if you want to print the board in the terminal.
        """
        lines = []

        for row in range(ROWS):
            pieces = []

            for col in range(COLS):
                value = self.board[row][col]

                if value == EMPTY:
                    pieces.append(".")
                elif value == PLAYER:
                    pieces.append("X")
                else:
                    pieces.append("O")

            lines.append(" ".join(pieces))

        header = " ".join(str(i + 1) for i in range(COLS))
        return "\n".join(lines) + "\n" + header