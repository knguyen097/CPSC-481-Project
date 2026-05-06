"""AI agent for Connect 4 using Minimax with Alpha-Beta Pruning.

This file handles the computer opponent's decision-making.
The AI can play at different difficulty levels:
- Easy: chooses a random valid move.
- Medium: uses Minimax with a smaller search depth.
- Hard: uses Minimax with a deeper search depth.

The Minimax algorithm simulates future moves and chooses the move
that gives the AI the best chance of winning.
Alpha-Beta Pruning improves Minimax by skipping branches that do not
need to be searched.
"""

import random

from connect4 import Connect4, ROWS, COLS, EMPTY, PLAYER, AI_PLAYER

# Large values are used so guaranteed wins/losses are ranked above normal board scores.
WIN_SCORE = 100000
LOSE_SCORE = -100000

def get_opponent(player):
    """Return the opposing player value."""
    return PLAYER if player == AI_PLAYER else AI_PLAYER

def order_moves(valid_moves):
    """Return valid moves in a stronger search order.

    In Connect 4, center columns are usually stronger because they create
    more possible horizontal and diagonal winning paths.

    Searching stronger moves first also helps Alpha-Beta Pruning cut off
    unnecessary branches faster.
    """
    preferred_order = [COLS // 2, 2, 4, 1, 5, 0, 6]
    return [col for col in preferred_order if col in valid_moves]

def score_window(window, player):
    """Score a group of four board spaces for the given player.

    A "window" is any group of four spaces that could become a Connect 4.
    This function rewards strong patterns for the AI and penalizes strong
    patterns for the opponent.
    """
    opponent = get_opponent(player)
    score = 0

    # Reward the player for creating winning or near-winning patterns.
    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(EMPTY) == 1:
        score += 8
    elif window.count(player) == 2 and window.count(EMPTY) == 2:
        score += 3

    # Penalize the score when the opponent has dangerous patterns.
    # This encourages the AI to block the player.
    if window.count(opponent) == 4:
        score -= 100
    elif window.count(opponent) == 3 and window.count(EMPTY) == 1:
        score -= 10
    elif window.count(opponent) == 2 and window.count(EMPTY) == 2:
        score -= 2

    return score

def evaluate_board(board, player):
    """Evaluate the current board from the given player's point of view.

    This function is used when Minimax reaches its search limit.
    Instead of knowing the final result of the game, it estimates how good
    the current board is for the AI.
    """
    score = 0

    # Favor the center column because it gives access to many winning lines.
    center_col = [board[row][COLS // 2] for row in range(ROWS)]
    score += center_col.count(player) * 6

    # Check all horizontal groups of four.
    for row in range(ROWS):
        for col in range(COLS - 3):
            window = board[row][col:col + 4]
            score += score_window(window, player)

    # Check all vertical groups of four.
    for col in range(COLS):
        column = [board[row][col] for row in range(ROWS)]

        for row in range(ROWS - 3):
            window = column[row:row + 4]
            score += score_window(window, player)

    # Check all diagonal groups going down and to the right.
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = [board[row + i][col + i] for i in range(4)]
            score += score_window(window, player)

    # Check all diagonal groups going up and to the right.
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            window = [board[row - i][col + i] for i in range(4)]
            score += score_window(window, player)

    return score

def find_winning_move(game, player):
    """Return a column that wins immediately, if one exists.

    This is checked before Minimax so the AI does not miss a guaranteed win
    or fail to block the player's immediate win.
    """
    for col in order_moves(game.valid_moves()):
        game_copy = game.copy()
        game_copy.drop_piece(col, player)

        if game_copy.check_win() == player:
            return col

    return None

def minimax(game, depth, alpha, beta, maximizing_player, player_id):
    """Use Minimax with Alpha-Beta Pruning to choose the best move.

    Args:
        game: Current Connect4 game state.
        depth: How many future moves the AI should simulate.
        alpha: Best score the maximizing player can guarantee so far.
        beta: Best score the minimizing player can guarantee so far.
        maximizing_player: True when it is the AI's simulated turn.
        player_id: The AI player value being evaluated.

    Returns:
        A tuple containing the best column and its score.
    """
    valid_moves = game.valid_moves()
    opponent = get_opponent(player_id)
    winner = game.check_win()

    # Case: the AI has won.
    # Adding depth rewards faster wins.
    if winner == player_id:
        return None, WIN_SCORE + depth

    # Case: the opponent has won.
    # Subtracting depth makes earlier losses worse than later losses.
    if winner == opponent:
        return None, LOSE_SCORE - depth

    # Case: the search limit was reached, the board is full,
    # or there are no valid moves left.
    if depth == 0 or game.is_full() or not valid_moves:
        return None, evaluate_board(game.board, player_id)

    ordered_valid_moves = order_moves(valid_moves)

    if maximizing_player:
        # The maximizing player is the AI.
        # It tries to find the move with the highest score.
        value = -float("inf")
        best_col = ordered_valid_moves[0]

        for col in ordered_valid_moves:
            game_copy = game.copy()
            game_copy.drop_piece(col, player_id)

            # After the AI move, simulate the opponent's response.
            new_score = minimax(
                game_copy,
                depth - 1,
                alpha,
                beta,
                False,
                player_id
            )[1]

            if new_score > value:
                value = new_score
                best_col = col

            # Alpha tracks the best score the AI can guarantee.
            alpha = max(alpha, value)

            # If alpha is greater than or equal to beta, this branch
            # cannot improve the result and can be skipped.
            if alpha >= beta:
                break

        return best_col, value

    # The minimizing player is the opponent.
    # It tries to find the move that gives the AI the lowest score.
    value = float("inf")
    best_col = ordered_valid_moves[0]

    for col in ordered_valid_moves:
        game_copy = game.copy()
        game_copy.drop_piece(col, opponent)

        # After the opponent move, simulate the AI's next response.
        new_score = minimax(
            game_copy,
            depth - 1,
            alpha,
            beta,
            True,
            player_id
        )[1]

        if new_score < value:
            value = new_score
            best_col = col

        # Beta tracks the best score the opponent can guarantee.
        beta = min(beta, value)

        # Stop searching this branch if it cannot affect the final decision.
        if alpha >= beta:
            break

    return best_col, value


def choose_move(game: Connect4, player_id: int, difficulty: str = "medium"):
    """Choose the AI's next move based on the selected difficulty."""
    valid_moves = game.valid_moves()

    if not valid_moves:
        return None

    # Easy mode does not use strategy.
    # It simply picks one of the available columns at random.
    if difficulty == "easy":
        return random.choice(valid_moves)

    # Always take an immediate winning move if one is available.
    winning_move = find_winning_move(game, player_id)

    if winning_move is not None:
        return winning_move

    # Always block the opponent if they can win on their next turn.
    opponent = get_opponent(player_id)
    blocking_move = find_winning_move(game, opponent)

    if blocking_move is not None:
        return blocking_move

    # Medium searches fewer moves ahead.
    # Hard searches deeper, making it stronger but slightly slower.
    if difficulty == "medium":
        depth = 2
    else:
        depth = 4

    col, _ = minimax(
        game,
        depth,
        -float("inf"),
        float("inf"),
        True,
        player_id
    )

    # Fallback safety check in case Minimax does not return a move.
    if col is None:
        return random.choice(valid_moves)

    return col