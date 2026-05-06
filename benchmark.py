#!/usr/bin/env python3
"""Detailed benchmark for Connect 4 Minimax vs Alpha-Beta Pruning.

This file is separate from the Pygame game.
It only prints benchmark results in the terminal.

It compares:
1. Traditional Minimax
2. Minimax with Alpha-Beta Pruning

Depths tested:
- Medium difficulty depth: 2
- Hard difficulty depth: 4
- Extra benchmark depth: 6

Run:
    python benchmark.py

Optional:
    python benchmark.py --repeats 5
    python benchmark.py --moves 0 6 12 18 24
"""

import argparse
import random
import statistics
import time

from ai import (
    LOSE_SCORE,
    WIN_SCORE,
    evaluate_board,
    get_opponent,
    order_moves,
)
from connect4 import Connect4, EMPTY, PLAYER, AI_PLAYER


TEST_DEPTHS = [
    ("Medium", 2),
    ("Hard", 4),
    ("Extra", 6),
]


def create_stats():
    """Create a dictionary for tracking search metrics."""
    return {
        "nodes": 0,
        "evals": 0,
        "terminal_wins": 0,
        "terminal_draws": 0,
        "decision_nodes": 0,
        "branches": 0,
        "cutoffs": 0,
    }


def count_pieces(game):
    """Return the number of non-empty spaces on the board."""
    total = 0

    for row in game.board:
        for value in row:
            if value != EMPTY:
                total += 1

    return total


def generate_random_position(move_count, seed):
    """Generate a legal board position with no current winner.

    The benchmark uses random board positions so the AI is tested at
    different stages of the game.
    """
    rng = random.Random(seed)

    for _ in range(500):
        game = Connect4()
        turn = PLAYER
        moves_played = 0

        while moves_played < move_count:
            valid_moves = game.valid_moves()

            if not valid_moves:
                break

            col = rng.choice(valid_moves)
            game.drop_piece(col, turn)
            moves_played += 1

            if game.check_win() != EMPTY:
                break

            if turn == PLAYER:
                turn = AI_PLAYER
            else:
                turn = PLAYER

        if moves_played == move_count and game.check_win() == EMPTY:
            return game

    return Connect4()


def build_test_positions(move_counts, seed):
    """Create test positions for the benchmark."""
    positions = []

    for index, move_count in enumerate(move_counts):
        game = generate_random_position(move_count, seed + index * 100)

        positions.append(
            {
                "name": f"{move_count} moves",
                "game": game,
                "pieces": count_pieces(game),
                "valid_moves": len(game.valid_moves()),
            }
        )

    return positions


def get_average_branching(stats):
    """Return the average number of available moves at decision nodes."""
    if stats["decision_nodes"] == 0:
        return 0

    return stats["branches"] / stats["decision_nodes"]


def minimax_without_pruning(game, depth, maximizing_player, player_id, stats):
    """Traditional Minimax with no Alpha-Beta Pruning.

    This version searches every possible branch until it reaches:
    - a win/loss,
    - a draw/full board,
    - or the selected depth limit.
    """
    stats["nodes"] += 1

    valid_moves = game.valid_moves()
    opponent = get_opponent(player_id)
    winner = game.check_win()

    if winner == player_id:
        stats["terminal_wins"] += 1
        return None, WIN_SCORE + depth

    if winner == opponent:
        stats["terminal_wins"] += 1
        return None, LOSE_SCORE - depth

    if game.is_full() or not valid_moves:
        stats["terminal_draws"] += 1
        return None, 0

    if depth == 0:
        stats["evals"] += 1
        return None, evaluate_board(game.board, player_id)

    ordered_valid_moves = order_moves(valid_moves)

    stats["decision_nodes"] += 1
    stats["branches"] += len(ordered_valid_moves)

    if maximizing_player:
        value = -float("inf")
        best_col = ordered_valid_moves[0]

        for col in ordered_valid_moves:
            game_copy = game.copy()
            game_copy.drop_piece(col, player_id)

            _, new_score = minimax_without_pruning(
                game_copy,
                depth - 1,
                False,
                player_id,
                stats,
            )

            if new_score > value:
                value = new_score
                best_col = col

        return best_col, value

    value = float("inf")
    best_col = ordered_valid_moves[0]

    for col in ordered_valid_moves:
        game_copy = game.copy()
        game_copy.drop_piece(col, opponent)

        _, new_score = minimax_without_pruning(
            game_copy,
            depth - 1,
            True,
            player_id,
            stats,
        )

        if new_score < value:
            value = new_score
            best_col = col

    return best_col, value


def minimax_with_pruning(game, depth, alpha, beta, maximizing_player, player_id, stats):
    """Minimax with Alpha-Beta Pruning.

    This version searches the same kind of game tree, but it stops early
    when a branch cannot improve the final decision.
    """
    stats["nodes"] += 1

    valid_moves = game.valid_moves()
    opponent = get_opponent(player_id)
    winner = game.check_win()

    if winner == player_id:
        stats["terminal_wins"] += 1
        return None, WIN_SCORE + depth

    if winner == opponent:
        stats["terminal_wins"] += 1
        return None, LOSE_SCORE - depth

    if game.is_full() or not valid_moves:
        stats["terminal_draws"] += 1
        return None, 0

    if depth == 0:
        stats["evals"] += 1
        return None, evaluate_board(game.board, player_id)

    ordered_valid_moves = order_moves(valid_moves)

    stats["decision_nodes"] += 1
    stats["branches"] += len(ordered_valid_moves)

    if maximizing_player:
        value = -float("inf")
        best_col = ordered_valid_moves[0]

        for col in ordered_valid_moves:
            game_copy = game.copy()
            game_copy.drop_piece(col, player_id)

            _, new_score = minimax_with_pruning(
                game_copy,
                depth - 1,
                alpha,
                beta,
                False,
                player_id,
                stats,
            )

            if new_score > value:
                value = new_score
                best_col = col

            alpha = max(alpha, value)

            if alpha >= beta:
                stats["cutoffs"] += 1
                break

        return best_col, value

    value = float("inf")
    best_col = ordered_valid_moves[0]

    for col in ordered_valid_moves:
        game_copy = game.copy()
        game_copy.drop_piece(col, opponent)

        _, new_score = minimax_with_pruning(
            game_copy,
            depth - 1,
            alpha,
            beta,
            True,
            player_id,
            stats,
        )

        if new_score < value:
            value = new_score
            best_col = col

        beta = min(beta, value)

        if alpha >= beta:
            stats["cutoffs"] += 1
            break

    return best_col, value


def run_single_test(game, depth, version):
    """Run one benchmark test and return timing and stats."""
    stats = create_stats()

    start_time = time.perf_counter()

    if version == "minimax":
        move, score = minimax_without_pruning(
            game,
            depth,
            True,
            AI_PLAYER,
            stats,
        )
    else:
        move, score = minimax_with_pruning(
            game,
            depth,
            -float("inf"),
            float("inf"),
            True,
            AI_PLAYER,
            stats,
        )

    end_time = time.perf_counter()

    elapsed_seconds = end_time - start_time
    elapsed_ms = elapsed_seconds * 1000

    if elapsed_seconds > 0:
        nodes_per_second = stats["nodes"] / elapsed_seconds
    else:
        nodes_per_second = 0

    terminal_total = stats["terminal_wins"] + stats["terminal_draws"]

    return {
        "elapsed_ms": elapsed_ms,
        "nodes": stats["nodes"],
        "nodes_per_second": nodes_per_second,
        "evals": stats["evals"],
        "terminal_wins": stats["terminal_wins"],
        "terminal_draws": stats["terminal_draws"],
        "terminal_total": terminal_total,
        "decision_nodes": stats["decision_nodes"],
        "branching": get_average_branching(stats),
        "cutoffs": stats["cutoffs"],
        "move": move,
        "score": score,
    }


def summarize_trial_results(trials):
    """Average repeated benchmark results."""
    return {
        "avg_ms": statistics.fmean(test["elapsed_ms"] for test in trials),
        "median_ms": statistics.median(test["elapsed_ms"] for test in trials),
        "min_ms": min(test["elapsed_ms"] for test in trials),
        "max_ms": max(test["elapsed_ms"] for test in trials),
        "avg_nodes": statistics.fmean(test["nodes"] for test in trials),
        "avg_nodes_per_second": statistics.fmean(
            test["nodes_per_second"] for test in trials
        ),
        "avg_evals": statistics.fmean(test["evals"] for test in trials),
        "avg_terminal_wins": statistics.fmean(
            test["terminal_wins"] for test in trials
        ),
        "avg_terminal_draws": statistics.fmean(
            test["terminal_draws"] for test in trials
        ),
        "avg_terminal_total": statistics.fmean(
            test["terminal_total"] for test in trials
        ),
        "avg_decision_nodes": statistics.fmean(
            test["decision_nodes"] for test in trials
        ),
        "avg_branching": statistics.fmean(test["branching"] for test in trials),
        "avg_cutoffs": statistics.fmean(test["cutoffs"] for test in trials),
        "last_move": trials[-1]["move"],
        "last_score": trials[-1]["score"],
    }


def benchmark(positions, repeats):
    """Run benchmark tests for all depths, positions, and algorithm versions."""
    detailed_results = []
    comparison_results = []

    for level_name, depth in TEST_DEPTHS:
        for position in positions:
            minimax_trials = []
            alpha_beta_trials = []

            for _ in range(repeats):
                minimax_game = position["game"].copy()
                alpha_beta_game = position["game"].copy()

                minimax_trials.append(
                    run_single_test(minimax_game, depth, "minimax")
                )

                alpha_beta_trials.append(
                    run_single_test(alpha_beta_game, depth, "alpha_beta")
                )

            minimax_summary = summarize_trial_results(minimax_trials)
            alpha_beta_summary = summarize_trial_results(alpha_beta_trials)

            detailed_results.append(
                {
                    "level": level_name,
                    "depth": depth,
                    "position": position["name"],
                    "pieces": position["pieces"],
                    "valid_moves": position["valid_moves"],
                    "version": "Traditional",
                    "trials": repeats,
                    **minimax_summary,
                }
            )

            detailed_results.append(
                {
                    "level": level_name,
                    "depth": depth,
                    "position": position["name"],
                    "pieces": position["pieces"],
                    "valid_moves": position["valid_moves"],
                    "version": "Alpha-Beta",
                    "trials": repeats,
                    **alpha_beta_summary,
                }
            )

            nodes_saved = (
                minimax_summary["avg_nodes"] - alpha_beta_summary["avg_nodes"]
            )

            if minimax_summary["avg_nodes"] > 0:
                node_save_percent = (
                    nodes_saved / minimax_summary["avg_nodes"]
                ) * 100
            else:
                node_save_percent = 0

            time_saved = (
                minimax_summary["avg_ms"] - alpha_beta_summary["avg_ms"]
            )

            if minimax_summary["avg_ms"] > 0:
                time_save_percent = (
                    time_saved / minimax_summary["avg_ms"]
                ) * 100
            else:
                time_save_percent = 0

            comparison_results.append(
                {
                    "level": level_name,
                    "depth": depth,
                    "position": position["name"],
                    "pieces": position["pieces"],
                    "valid_moves": position["valid_moves"],
                    "trials": repeats,
                    "minimax_nodes": minimax_summary["avg_nodes"],
                    "alpha_beta_nodes": alpha_beta_summary["avg_nodes"],
                    "nodes_saved": nodes_saved,
                    "node_save_percent": node_save_percent,
                    "minimax_ms": minimax_summary["avg_ms"],
                    "alpha_beta_ms": alpha_beta_summary["avg_ms"],
                    "time_saved": time_saved,
                    "time_save_percent": time_save_percent,
                    "alpha_beta_cutoffs": alpha_beta_summary["avg_cutoffs"],
                }
            )

    return detailed_results, comparison_results


def print_position_summary(positions):
    """Print the board positions used in the benchmark."""
    print("\nTEST POSITIONS")
    print("-" * 60)
    print(f"{'Position':<15} {'Pieces':>8} {'Valid Moves':>12}")
    print("-" * 60)

    for position in positions:
        print(
            f"{position['name']:<15} "
            f"{position['pieces']:>8} "
            f"{position['valid_moves']:>12}"
        )


def print_detailed_results(results):
    """Print detailed benchmark results for each algorithm version."""
    print("\nDETAILED RESULTS BY VERSION")
    print("-" * 185)

    print(
        f"{'Level':<8} "
        f"{'Depth':>5} "
        f"{'Position':<12} "
        f"{'Version':<13} "
        f"{'Trials':>6} "
        f"{'Avg ms':>10} "
        f"{'Median':>10} "
        f"{'Min':>10} "
        f"{'Max':>10} "
        f"{'Avg Nodes':>12} "
        f"{'Nodes/sec':>12} "
        f"{'Evals':>9} "
        f"{'Terminal':>9} "
        f"{'Decisions':>10} "
        f"{'Branch':>8} "
        f"{'Cutoffs':>9} "
        f"{'Move':>6} "
        f"{'Score':>8}"
    )

    print("-" * 185)

    for row in results:
        print(
            f"{row['level']:<8} "
            f"{row['depth']:>5} "
            f"{row['position']:<12} "
            f"{row['version']:<13} "
            f"{row['trials']:>6} "
            f"{row['avg_ms']:>10.3f} "
            f"{row['median_ms']:>10.3f} "
            f"{row['min_ms']:>10.3f} "
            f"{row['max_ms']:>10.3f} "
            f"{row['avg_nodes']:>12.1f} "
            f"{row['avg_nodes_per_second']:>12.0f} "
            f"{row['avg_evals']:>9.1f} "
            f"{row['avg_terminal_total']:>9.1f} "
            f"{row['avg_decision_nodes']:>10.1f} "
            f"{row['avg_branching']:>8.2f} "
            f"{row['avg_cutoffs']:>9.1f} "
            f"{str(row['last_move']):>6} "
            f"{row['last_score']:>8.1f}"
        )


def print_comparison_results(results):
    """Print side-by-side comparison of Minimax and Alpha-Beta."""
    print("\nTRADITIONAL MINIMAX VS ALPHA-BETA SUMMARY")
    print("-" * 160)

    print(
        f"{'Level':<8} "
        f"{'Depth':>5} "
        f"{'Position':<12} "
        f"{'Trials':>6} "
        f"{'Mini Nodes':>12} "
        f"{'AB Nodes':>12} "
        f"{'Nodes Saved':>13} "
        f"{'Node Save %':>12} "
        f"{'Mini ms':>10} "
        f"{'AB ms':>10} "
        f"{'Time Saved':>11} "
        f"{'Time Save %':>12} "
        f"{'AB Cutoffs':>11}"
    )

    print("-" * 160)

    for row in results:
        print(
            f"{row['level']:<8} "
            f"{row['depth']:>5} "
            f"{row['position']:<12} "
            f"{row['trials']:>6} "
            f"{row['minimax_nodes']:>12.1f} "
            f"{row['alpha_beta_nodes']:>12.1f} "
            f"{row['nodes_saved']:>13.1f} "
            f"{row['node_save_percent']:>11.1f}% "
            f"{row['minimax_ms']:>10.3f} "
            f"{row['alpha_beta_ms']:>10.3f} "
            f"{row['time_saved']:>11.3f} "
            f"{row['time_save_percent']:>11.1f}% "
            f"{row['alpha_beta_cutoffs']:>11.1f}"
        )


def print_metric_notes():
    """Print explanations for the benchmark columns."""
    print("\nMETRIC NOTES")
    print("-" * 70)
    print("Avg ms      = average computational time to choose a move.")
    print("Median      = middle response time across repeated runs.")
    print("Min / Max   = fastest and slowest response time.")
    print("Avg Nodes   = average number of board states searched.")
    print("Nodes/sec   = how many board states were searched per second.")
    print("Evals       = heuristic board evaluations at the depth limit.")
    print("Terminal    = simulated states where the game was already over.")
    print("Decisions   = nodes where the algorithm had to choose among moves.")
    print("Branch      = average number of valid moves at decision nodes.")
    print("Cutoffs     = Alpha-Beta pruning events. Traditional Minimax has 0.")
    print("Move        = column selected by the algorithm.")
    print("Score       = final Minimax score for the selected move.")


def main():
    """Run the benchmark from the terminal."""
    parser = argparse.ArgumentParser(
        description="Detailed Connect 4 AI benchmark."
    )

    parser.add_argument(
        "--repeats",
        type=int,
        default=3,
        help="Number of times to repeat each test.",
    )

    parser.add_argument(
        "--moves",
        type=int,
        nargs="+",
        default=[0, 6, 12, 18, 24],
        help="Board positions to test by number of moves already played.",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed used to create repeatable board positions.",
    )

    args = parser.parse_args()

    print("\nCONNECT 4 AI DETAILED BENCHMARK")
    print("=" * 70)
    print("Testing preset AI depths plus one extra depth:")
    print("Medium = depth 2")
    print("Hard   = depth 4")
    print("Extra  = depth 6")
    print(f"Repeats per test: {args.repeats}")
    print(f"Move counts tested: {args.moves}")
    print(f"Random seed: {args.seed}")

    positions = build_test_positions(args.moves, args.seed)

    print_position_summary(positions)

    detailed_results, comparison_results = benchmark(positions, args.repeats)

    print_detailed_results(detailed_results)
    print_comparison_results(comparison_results)
    print_metric_notes()

    print("\nDone.")


if __name__ == "__main__":
    main()