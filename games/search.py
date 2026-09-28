"""
A game-agnostic negamax search with alpha-beta pruning.

The search knows nothing about any particular game. It operates on any object
that satisfies the :class:`GameState` protocol below, so the identical search
code drives both Connect Four (see ``games/connect_four.py``) and the existing
Tic-Tac-Toe engine (via the adapter in ``games/tictactoe_adapter.py``).

Scores are always from the perspective of the side to move; the recursive
result is negated to flip perspective between plies (the "nega" in negamax).
Because of that convention, a terminal position is always a loss (or draw) for
the side to move: the opponent completed the winning line on the previous ply.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Protocol, Tuple, TypeVar, runtime_checkable

Move = TypeVar("Move")


@runtime_checkable
class GameState(Protocol):
    """The minimal interface the negamax search needs from a game."""

    def is_terminal(self) -> bool:
        """True if the game is over (a win just occurred, or no moves remain)."""
        ...

    def score(self) -> float:
        """Value from the side-to-move's perspective.

        At a terminal node this is the decided outcome (a loss for the mover,
        or a draw); otherwise it is a heuristic estimate. Terminal magnitudes
        must dominate every heuristic value the game can return.
        """
        ...

    def legal_moves(self) -> list:
        """Moves available to the side to move."""
        ...

    def make_move(self, move) -> "GameState":
        """Return the successor state after playing ``move`` (no mutation)."""
        ...

    def order_moves(self) -> list:
        """Moves in search order. Good ordering makes alpha-beta prune harder."""
        ...


@dataclass
class SearchStats:
    nodes: int = 0

    def __str__(self) -> str:
        return f"nodes={self.nodes}"


def negamax(
    state: GameState,
    depth: int,
    alpha: float = float("-inf"),
    beta: float = float("inf"),
    stats: Optional[SearchStats] = None,
) -> Tuple[float, Optional[object]]:
    """Return (value, best_move) for ``state`` searched to ``depth`` plies.

    ``value`` is from the side-to-move's perspective. ``best_move`` is None at
    a leaf or terminal node.
    """
    if stats is not None:
        stats.nodes += 1

    if state.is_terminal() or depth == 0:
        return state.score(), None

    best_value = float("-inf")
    best_move: Optional[object] = None

    for move in state.order_moves():
        child = state.make_move(move)
        value = -negamax(child, depth - 1, -beta, -alpha, stats)[0]
        if value > best_value:
            best_value = value
            best_move = move
        alpha = max(alpha, value)
        if alpha >= beta:
            break  # this branch cannot improve the caller's outcome

    return best_value, best_move
