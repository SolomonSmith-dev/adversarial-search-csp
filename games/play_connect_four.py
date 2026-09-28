"""
Headless terminal driver for Connect Four, powered by the game-agnostic
negamax search in ``games/search.py``.

Examples:
    python3 games/play_connect_four.py                    # human (X) vs AI
    python3 games/play_connect_four.py --mode ai_vs_ai     # watch the AI play
    python3 games/play_connect_four.py --rows 6 --cols 7 --connect 4 --depth 5
"""
from __future__ import annotations

import argparse
from typing import Optional

from connect_four import SYMBOLS, ConnectFour
from search import SearchStats, negamax


def ai_move(state: ConnectFour, depth: int):
    """Return the AI's chosen column (and node count) for the side to move."""
    stats = SearchStats()
    _, move = negamax(state, depth=depth, stats=stats)
    if move is None:  # depth 0 or no ordering surfaced a move; fall back
        move = state.order_moves()[0]
    return move, stats


def human_move(state: ConnectFour) -> int:
    legal = state.legal_moves()
    while True:
        raw = input(f"Drop into which column {legal}? ").strip()
        try:
            col = int(raw)
        except ValueError:
            print("  Enter a column number.")
            continue
        if col in legal:
            return col
        print("  That column is full or off-board.")


def play(rows=6, cols=7, connect=4, mode="human_vs_ai", human_symbol="X",
         depth=5, move_fn=None, out=print):
    """Play one game to completion; return the winner string ('X'/'O'/'DRAW')."""
    if move_fn is None:
        move_fn = human_move

    state = ConnectFour(rows=rows, cols=cols, connect=connect)
    out(state.render())
    while not state.is_terminal():
        side = SYMBOLS[state.current_player]
        if mode == "human_vs_ai" and side == human_symbol:
            col = move_fn(state)
        else:
            col, stats = ai_move(state, depth)
            out(f"AI ({side}) drops column {col}  [{stats}]")
        state = state.make_move(col)
        out(state.render())
        out("=" * (2 * cols - 1))

    out(f"Result: {state.winner}")
    return state.winner


def main(argv: Optional[list] = None) -> None:
    parser = argparse.ArgumentParser(description="Headless Connect Four.")
    parser.add_argument("--rows", type=int, default=6)
    parser.add_argument("--cols", type=int, default=7)
    parser.add_argument("--connect", type=int, default=4,
                        help="pieces in a row needed to win (default: 4)")
    parser.add_argument("--mode", default="human_vs_ai",
                        choices=["human_vs_ai", "ai_vs_ai"])
    parser.add_argument("--symbol", default="X", choices=["X", "O"],
                        help="human symbol; X moves first (default: X)")
    parser.add_argument("--depth", type=int, default=5,
                        help="search depth in plies (default: 5)")
    args = parser.parse_args(argv)

    play(rows=args.rows, cols=args.cols, connect=args.connect, mode=args.mode,
         human_symbol=args.symbol, depth=args.depth)


if __name__ == "__main__":
    main()
