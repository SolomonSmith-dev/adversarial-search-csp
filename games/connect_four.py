"""
Connect Four as a :class:`games.search.GameState`.

The same negamax search that plays Tic-Tac-Toe drives this game unchanged; all
Connect-Four-specific knowledge (gravity, win detection, the heuristic) lives
here. Internally a piece is +1 or -1 and ``current_player`` is the side to move,
which keeps every score mover-relative as negamax requires.

Examples:
    python3 games/play_connect_four.py                 # human (X) vs AI
    python3 games/play_connect_four.py --mode ai_vs_ai --depth 5
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

WIN_SCORE = 1_000_000  # dominates any heuristic value the eval can return

# Piece encoding and display.
SYMBOLS = {0: ".", 1: "X", -1: "O"}

# Heuristic weights for a length-`connect` window occupied by one player only.
_MY_WINDOW = {1: 1, 2: 10, 3: 50}
_OPP_WINDOW = {1: 1, 2: 10, 3: 80}  # opponent threats weighted slightly higher


class ConnectFour:
    def __init__(
        self,
        rows: int = 6,
        cols: int = 7,
        connect: int = 4,
        board: Optional[List[List[int]]] = None,
        current_player: int = 1,
    ):
        self.rows = rows
        self.cols = cols
        self.connect = connect
        self.current_player = current_player
        self.board = board if board is not None else [[0] * cols for _ in range(rows)]

    # ---- core mechanics ------------------------------------------------
    def legal_moves(self) -> List[int]:
        """Columns that are not yet full (top cell empty)."""
        return [c for c in range(self.cols) if self.board[0][c] == 0]

    def order_moves(self) -> List[int]:
        """Center-out column order — the strongest generic Connect Four
        ordering, which also helps alpha-beta prune."""
        mid = (self.cols - 1) / 2
        return sorted(self.legal_moves(), key=lambda c: abs(c - mid))

    def make_move(self, col: int) -> "ConnectFour":
        """Drop the current player's piece into ``col`` (gravity), flip turn."""
        if self.board[0][col] != 0:
            raise ValueError(f"Column {col} is full.")
        new_board = [row[:] for row in self.board]
        for r in range(self.rows - 1, -1, -1):
            if new_board[r][col] == 0:
                new_board[r][col] = self.current_player
                break
        return ConnectFour(self.rows, self.cols, self.connect, new_board,
                           -self.current_player)

    # ---- win detection -------------------------------------------------
    def _windows(self):
        """Yield every length-`connect` line (horizontal, vertical, both diagonals)."""
        L, B = self.connect, self.board
        R, C = self.rows, self.cols
        for r in range(R):
            for c in range(C - L + 1):
                yield [B[r][c + k] for k in range(L)]
        for c in range(C):
            for r in range(R - L + 1):
                yield [B[r + k][c] for k in range(L)]
        for r in range(R - L + 1):
            for c in range(C - L + 1):
                yield [B[r + k][c + k] for k in range(L)]
        for r in range(R - L + 1):
            for c in range(L - 1, C):
                yield [B[r + k][c - k] for k in range(L)]

    def winner_value(self) -> int:
        """+1 or -1 for the player with `connect` in a row, else 0."""
        for window in self._windows():
            first = window[0]
            if first != 0 and all(v == first for v in window):
                return first
        return 0

    def is_full(self) -> bool:
        return all(self.board[0][c] != 0 for c in range(self.cols))

    def is_terminal(self) -> bool:
        return self.winner_value() != 0 or self.is_full()

    @property
    def winner(self) -> Optional[str]:
        """Human-readable outcome: 'X', 'O', 'DRAW', or None if unfinished."""
        w = self.winner_value()
        if w != 0:
            return SYMBOLS[w]
        return "DRAW" if self.is_full() else None

    # ---- evaluation (mover-relative) -----------------------------------
    def _score_window(self, window: List[int], me: int) -> int:
        opp = -me
        has_me, has_opp = me in window, opp in window
        if has_me and has_opp:
            return 0  # blocked line, no potential for either side
        if has_me:
            return _MY_WINDOW.get(window.count(me), 0)
        if has_opp:
            return -_OPP_WINDOW.get(window.count(opp), 0)
        return 0

    def score(self) -> float:
        """Value from the side-to-move's perspective."""
        if self.winner_value() != 0:
            # A finished line means the opponent moved last and won, so the
            # side to move has lost.
            return -WIN_SCORE
        if self.is_full():
            return 0  # draw
        me = self.current_player
        total = sum(self._score_window(w, me) for w in self._windows())
        # Small bonus for central column control.
        center = self.cols // 2
        for r in range(self.rows):
            if self.board[r][center] == me:
                total += 3
            elif self.board[r][center] == -me:
                total -= 3
        return total

    # ---- rendering -----------------------------------------------------
    def render(self) -> str:
        rows = [" ".join(SYMBOLS[v] for v in row) for row in self.board]
        footer = " ".join(str(c) for c in range(self.cols))
        return "\n".join(rows + ["-" * (2 * self.cols - 1), footer])
