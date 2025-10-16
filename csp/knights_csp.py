"""
CSP: Place k knights on an n x n chessboard so that no two attack each other.

Formulation
- Variables: K1..Kk (one for each knight)
- Domain: all board positions (i, j) with 0 <= i, j < n
- Constraints:
  - All-different: no two knights on the same square
  - Non-attacking: no pair (Ki, Kj) are in a knight-move relation

Includes a simple backtracking solver and a demo in __main__.
"""
from __future__ import annotations
from typing import List, Tuple, Dict, Optional, Set

Position = Tuple[int, int]


def knight_attacks(a: Position, b: Position) -> bool:
    dr = abs(a[0] - b[0])
    dc = abs(a[1] - b[1])
    return (dr == 2 and dc == 1) or (dr == 1 and dc == 2)


def backtrack_knights(n: int, k: int) -> Optional[List[Position]]:
    """Simple backtracking to place k knights on n x n without conflicts."""
    solution: List[Position] = []
    used: Set[Position] = set()

    def is_safe(pos: Position) -> bool:
        if pos in used:
            return False
        for q in solution:
            if knight_attacks(pos, q):
                return False
        return True

    def bt(start_idx: int) -> bool:
        if len(solution) == k:
            return True
        for idx in range(start_idx, n * n):
            r, c = divmod(idx, n)
            pos = (r, c)
            if is_safe(pos):
                solution.append(pos)
                used.add(pos)
                if bt(idx + 1):
                    return True
                used.remove(pos)
                solution.pop()
        return False

    found = bt(0)
    return solution if found else None


def pretty_board(n: int, placements: List[Position]) -> str:
    board = [["." for _ in range(n)] for _ in range(n)]
    for (r, c) in placements:
        board[r][c] = "N"
    return "\n".join(" ".join(row) for row in board)


if __name__ == "__main__":
    # Demo: small instance
    n, k = 5, 5
    sol = backtrack_knights(n, k)
    if sol:
        print(f"Found placement for {k} knights on {n}x{n} board:")
        print(pretty_board(n, sol))
    else:
        print("No solution found.")
