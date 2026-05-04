"""Connect 4 game logic.

This file does not depend on the terminal or Pygame.
It only handles the board, valid moves, piece dropping, and win checking.
"""

ROWS = 6
COLS = 7

EMPTY = 0
PLAYER = 1
AI_PLAYER = 2


class Connect4:
    def __init__(self):
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

    def reset(self):
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

    def copy(self):
        new_game = Connect4()
        new_game.board = [row[:] for row in self.board]
        return new_game

    def valid_moves(self):
        return [col for col in range(COLS) if self.board[0][col] == EMPTY]

    def is_valid_move(self, col):
        if col is None:
            return False

        return 0 <= col < COLS and self.board[0][col] == EMPTY
    
    def get_drop_row(self, col):
        """Return the row where a piece would land in the given column.

        Returns None if the column is invalid or full.
        """
        if col is None:
            return None

        if not self.is_valid_move(col):
            return None

        for row in range(ROWS - 1, -1, -1):
            if self.board[row][col] == EMPTY:
                return row

        return None

    def drop_piece(self, col, player):
        """Drop a piece into a column.

        Returns True if the move worked.
        Returns False if the column is full or out of range.
        """
        if not self.is_valid_move(col):
            return False

        for row in range(ROWS - 1, -1, -1):
            if self.board[row][col] == EMPTY:
                self.board[row][col] = player
                return True

        return False

    def is_full(self):
        return all(self.board[0][col] != EMPTY for col in range(COLS))

    def check_win(self):
        """Return 0 for no winner, 1 for player, or 2 for AI."""
        for row in range(ROWS):
            for col in range(COLS):
                player = self.board[row][col]

                if player == EMPTY:
                    continue

                # Horizontal
                if col <= COLS - 4 and all(self.board[row][col + i] == player for i in range(4)):
                    return player

                # Vertical
                if row <= ROWS - 4 and all(self.board[row + i][col] == player for i in range(4)):
                    return player

                # Diagonal down-right
                if row <= ROWS - 4 and col <= COLS - 4 and all(self.board[row + i][col + i] == player for i in range(4)):
                    return player

                # Diagonal up-right
                if row >= 3 and col <= COLS - 4 and all(self.board[row - i][col + i] == player for i in range(4)):
                    return player

        return EMPTY

    def winning_cells(self):
        """Return the four winning board positions so the UI can highlight them."""
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

                    for i in range(4):
                        next_row = row + row_step * i
                        next_col = col + col_step * i

                        if 0 <= next_row < ROWS and 0 <= next_col < COLS:
                            cells.append((next_row, next_col))

                    if len(cells) == 4 and all(self.board[r][c] == player for r, c in cells):
                        return cells

        return []

    def render(self):
        """Optional text rendering for debugging only.

        The Pygame version does not use this during normal gameplay.
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