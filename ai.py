"""AI agent for Connect 4 with multiple difficulty levels."""
import random
from connect4 import Connect4, ROWS, COLS


def score_window(window, player):
    opp = 1 if player == 2 else 2
    score = 0
    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(player) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opp) == 3 and window.count(0) == 1:
        score -= 4
    return score


def evaluate_board(board, player):
    score = 0
    # center column preference
    center_col = [board[r][COLS//2] for r in range(ROWS)]
    score += center_col.count(player) * 3

    # horizontal
    for r in range(ROWS):
        row = board[r]
        for c in range(COLS-3):
            window = row[c:c+4]
            score += score_window(window, player)

    # vertical
    for c in range(COLS):
        col = [board[r][c] for r in range(ROWS)]
        for r in range(ROWS-3):
            window = col[r:r+4]
            score += score_window(window, player)

    # diag down-right
    for r in range(ROWS-3):
        for c in range(COLS-3):
            window = [board[r+i][c+i] for i in range(4)]
            score += score_window(window, player)

    # diag up-right
    for r in range(3, ROWS):
        for c in range(COLS-3):
            window = [board[r-i][c+i] for i in range(4)]
            score += score_window(window, player)

    return score


def is_terminal_node(game):
    return game.check_win() != 0 or game.is_full()


def minimax(game, depth, alpha, beta, maximizingPlayer, player_id):
    valid_locations = game.valid_moves()
    is_terminal = is_terminal_node(game)
    opp = 1 if player_id == 2 else 2

    if depth == 0 or is_terminal:
        winner = game.check_win()
        if winner == player_id:
            return (None, 100000000000000)
        elif winner == opp:
            return (None, -10000000000000)
        else:
            return (None, evaluate_board(game.board, player_id))

    if maximizingPlayer:
        value = -float('inf')
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            g = game.copy()
            g.drop_piece(col, player_id)
            new_score = minimax(g, depth-1, alpha, beta, False, player_id)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = float('inf')
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            g = game.copy()
            g.drop_piece(col, opp)
            new_score = minimax(g, depth-1, alpha, beta, True, player_id)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value


def choose_move(game: Connect4, player_id: int, difficulty: str = 'medium'):
    valid = game.valid_moves()
    if difficulty == 'easy':
        return random.choice(valid)
    if difficulty == 'medium':
        depth = 3
    else:
        depth = 5

    col, _ = minimax(game, depth, -float('inf'), float('inf'), True, player_id)
    if col is None:
        return random.choice(valid)
    return col
