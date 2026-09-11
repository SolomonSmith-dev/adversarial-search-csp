"""
Adapter presenting the existing Tic-Tac-Toe ``GameStatus`` engine as a
:class:`games.search.GameState`, so the game-agnostic negamax in
``games/search.py`` can drive it — the same search that plays Connect Four.

This is the concrete demonstration that the search core is game-agnostic: no
Tic-Tac-Toe logic is duplicated here, only translated to the protocol.
"""
from __future__ import annotations

from typing import List, Tuple

from game_status import GameStatus
from multiAgents import ordered_moves


class TicTacToeState:
    def __init__(self, game_status: GameStatus):
        self.gs = game_status

    def is_terminal(self) -> bool:
        return self.gs.is_terminal()

    def score(self) -> float:
        # get_negamax_scores is already mover-relative: a decided game is a
        # loss for the side to move; a non-terminal leaf is the heuristic.
        return self.gs.get_negamax_scores(self.gs.is_terminal())

    def legal_moves(self) -> List[Tuple[int, int]]:
        return self.gs.get_moves()

    def order_moves(self) -> List[Tuple[int, int]]:
        return ordered_moves(self.gs)

    def make_move(self, move) -> "TicTacToeState":
        return TicTacToeState(self.gs.get_new_state(move))
