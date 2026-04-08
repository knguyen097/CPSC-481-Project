"""Connect 4 game logic."""
ROWS = 6
COLS = 7

class Connect4:
    def __init__(self):
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    def copy(self):
        g = Connect4()
        g.board = [row[:] for row in self.board]
        return g

    def valid_moves(self):
        return [c for c in range(COLS) if self.board[0][c] == 0]

    def drop_piece(self, col, player):
        if col < 0 or col >= COLS or self.board[0][col] != 0:
            return False
        for r in range(ROWS-1, -1, -1):
            if self.board[r][col] == 0:
                self.board[r][col] = player
                return True
        return False

    def is_full(self):
        return all(self.board[0][c] != 0 for c in range(COLS))

    def _check_direction(self, start_r, start_c, dr, dc):
        player = self.board[start_r][start_c]
        if player == 0:
            return False
        r, c = start_r, start_c
        count = 0
        while 0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] == player:
            count += 1
            r += dr; c += dc
        return count

    def check_win(self):
        # returns 0 = no win, 1 or 2 for winner
        for r in range(ROWS):
            for c in range(COLS):
                p = self.board[r][c]
                if p == 0:
                    continue
                # check horizontal
                if c <= COLS-4 and all(self.board[r][c+i] == p for i in range(4)):
                    return p
                # vertical
                if r <= ROWS-4 and all(self.board[r+i][c] == p for i in range(4)):
                    return p
                # diag down-right
                if r <= ROWS-4 and c <= COLS-4 and all(self.board[r+i][c+i] == p for i in range(4)):
                    return p
                # diag up-right
                if r >= 3 and c <= COLS-4 and all(self.board[r-i][c+i] == p for i in range(4)):
                    return p
        return 0

    def render(self):
        lines = []
        for r in range(ROWS):
            row = []
            for c in range(COLS):
                v = self.board[r][c]
                if v == 0:
                    row.append('.')
                elif v == 1:
                    row.append('X')
                else:
                    row.append('O')
            lines.append(' '.join(row))
        header = ' '.join(str(i+1) for i in range(COLS))
        return '\n'.join(lines) + '\n' + header
