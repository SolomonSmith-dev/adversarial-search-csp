"""Headless terminal Tic-Tac-Toe driver.

Runs the same GameStatus engine and minimax/negamax search used by the GUI,
but in the terminal with no Pygame dependency. Supports human-vs-AI and
AI-vs-AI play on 3x3, 4x4, and 5x5 boards.

Examples:
    python3 tictactoe/play_cli.py                  # human (X) vs AI on 3x3
    python3 tictactoe/play_cli.py --mode ai_vs_ai  # watch two AIs play
    python3 tictactoe/play_cli.py --size 4 --depth 3 --algorithm minimax
"""
from __future__ import annotations

import argparse

from game_status import GameStatus
from multiAgents import minimax, negamax

# Board encoding: 1 == 'O', -1 == 'X', 0 == empty.
SYMBOLS = {0: ".", 1: "O", -1: "X"}


def render(state):
    """Return the board as a human-readable grid string."""
    rows = [" ".join(SYMBOLS[v] for v in row) for row in state.board_state]
    return "\n".join(rows)


def ai_move(state, algorithm, depth):
    """Pick the AI move for the side to move using the chosen search."""
    if algorithm == "minimax":
        # minimax expects "maximizing_player"; MAX is the human side (X by
        # convention), so the AI maximizes only when it is the human side.
        maximizing = (state.turn_O and state.human_symbol == "O") or (
            not state.turn_O and state.human_symbol == "X"
        )
        _, move = minimax(state, depth=depth, maximizing_player=maximizing)
    else:
        _, move = negamax(state, depth=depth)
    return move


def human_move(state):
    """Prompt for a `row col` move until a legal one is entered."""
    legal = set(state.get_moves())
    while True:
        raw = input("Your move as 'row col' (0-indexed): ").strip()
        try:
            r, c = (int(x) for x in raw.split())
        except ValueError:
            print("  Enter two integers separated by a space.")
            continue
        if (r, c) in legal:
            return (r, c)
        print("  That cell is off-board or already taken.")


def play(size=3, mode="human_vs_ai", human_symbol="X", algorithm="negamax",
         depth=4, move_fn=None, out=print):
    """Play one game to completion and return the GameStatus winner string.

    `move_fn` lets callers (e.g. tests) inject moves instead of reading stdin.
    `out` is the print-like sink for board/status output.
    """
    if move_fn is None:
        move_fn = human_move

    board = [[0] * size for _ in range(size)]
    # turn_O True means 'O' moves; X always goes first.
    state = GameStatus(board, turn_O=False, human_symbol=human_symbol)

    out(render(state))
    while not state.is_terminal():
        side = "O" if state.turn_O else "X"
        is_human = mode == "human_vs_ai" and side == human_symbol
        if is_human:
            move = move_fn(state)
        else:
            move = ai_move(state, algorithm, depth)
            out(f"AI ({side}) plays {move}")
        state = state.get_new_state(move)
        out(render(state))
        out("-" * (2 * size))

    out(f"Result: {state.winner}")
    return state.winner


def main(argv=None):
    parser = argparse.ArgumentParser(description="Headless Tic-Tac-Toe.")
    parser.add_argument("--size", type=int, default=3, choices=[3, 4, 5],
                        help="board size (default: 3)")
    parser.add_argument("--mode", default="human_vs_ai",
                        choices=["human_vs_ai", "ai_vs_ai"],
                        help="game mode (default: human_vs_ai)")
    parser.add_argument("--symbol", default="X", choices=["X", "O"],
                        help="human symbol; X moves first (default: X)")
    parser.add_argument("--algorithm", default="negamax",
                        choices=["minimax", "negamax"],
                        help="search algorithm for the AI (default: negamax)")
    parser.add_argument("--depth", type=int, default=4,
                        help="search depth (default: 4)")
    args = parser.parse_args(argv)

    play(size=args.size, mode=args.mode, human_symbol=args.symbol,
         algorithm=args.algorithm, depth=args.depth)


if __name__ == "__main__":
    main()
