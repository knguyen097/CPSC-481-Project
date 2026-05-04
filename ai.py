"""AI agent for Connect 4 using minimax with alpha-beta pruning."""

import random

from connect4 import Connect4, ROWS, COLS, EMPTY, PLAYER, AI_PLAYER

WIN_SCORE = 1_000_000_000
LOSE_SCORE = -1_000_000_000

def get_opponent(player):
    return PLAYER if player == AI_PLAYER else AI_PLAYER

def order_moves(valid_moves):
    """Search center columns first to make alpha-beta pruning more effective."""
    preferred_order = [COLS // 2, 2, 4, 1, 5, 0, 6]
    return [col for col in preferred_order if col in valid_moves]

def score_window(window, player):
    opponent = get_opponent(player)
    score = 0

    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(EMPTY) == 1:
        score += 8
    elif window.count(player) == 2 and window.count(EMPTY) == 2:
        score += 3

    # Blocking the opponent is very important in Connect 4.
    if window.count(opponent) == 4:
        score -= 100
    elif window.count(opponent) == 3 and window.count(EMPTY) == 1:
        score -= 10
    elif window.count(opponent) == 2 and window.count(EMPTY) == 2:
        score -= 2

    return score

def evaluate_board(board, player):
    score = 0

    # Favor the center column because it creates more possible winning lines.
    center_col = [board[row][COLS // 2] for row in range(ROWS)]
    score += center_col.count(player) * 6

    # Horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            window = board[row][col:col + 4]
            score += score_window(window, player)

    # Vertical
    for col in range(COLS):
        column = [board[row][col] for row in range(ROWS)]

        for row in range(ROWS - 3):
            window = column[row:row + 4]
            score += score_window(window, player)

    # Diagonal down-right
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = [board[row + i][col + i] for i in range(4)]
            score += score_window(window, player)

    # Diagonal up-right
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            window = [board[row - i][col + i] for i in range(4)]
            score += score_window(window, player)

    return score

def find_winning_move(game, player):
    """Return a column that wins immediately, if one exists."""
    for col in order_moves(game.valid_moves()):
        game_copy = game.copy()
        game_copy.drop_piece(col, player)

        if game_copy.check_win() == player:
            return col

    return None

def minimax(game, depth, alpha, beta, maximizing_player, player_id):
    valid_moves = game.valid_moves()
    opponent = get_opponent(player_id)
    winner = game.check_win()

    if winner == player_id:
        return None, WIN_SCORE + depth

    if winner == opponent:
        return None, LOSE_SCORE - depth

    if depth == 0 or game.is_full() or not valid_moves:
        return None, evaluate_board(game.board, player_id)

    ordered_valid_moves = order_moves(valid_moves)

    if maximizing_player:
        value = -float("inf")
        best_col = ordered_valid_moves[0]

        for col in ordered_valid_moves:
            game_copy = game.copy()
            game_copy.drop_piece(col, player_id)

            new_score = minimax(game_copy, depth - 1, alpha, beta, False, player_id)[1]

            if new_score > value:
                value = new_score
                best_col = col

            alpha = max(alpha, value)

            if alpha >= beta:
                break

        return best_col, value

    value = float("inf")
    best_col = ordered_valid_moves[0]

    for col in ordered_valid_moves:
        game_copy = game.copy()
        game_copy.drop_piece(col, opponent)

        new_score = minimax(game_copy, depth - 1, alpha, beta, True, player_id)[1]

        if new_score < value:
            value = new_score
            best_col = col

        beta = min(beta, value)

        if alpha >= beta:
            break

    return best_col, value

def choose_move(game: Connect4, player_id: int, difficulty: str = "medium"):
    valid_moves = game.valid_moves()

    if not valid_moves:
        return None

    if difficulty == "easy":
        return random.choice(valid_moves)

    # Always take an immediate winning move.
    winning_move = find_winning_move(game, player_id)

    if winning_move is not None:
        return winning_move

    # Always block the opponent if they can win next turn.
    opponent = get_opponent(player_id)
    blocking_move = find_winning_move(game, opponent)

    if blocking_move is not None:
        return blocking_move

    if difficulty == "medium":
        depth = 3
    else:
        depth = 5

    col, _ = minimax(game, depth, -float("inf"), float("inf"), True, player_id)

    if col is None:
        return random.choice(valid_moves)

    return col