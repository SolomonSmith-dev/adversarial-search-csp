"""
Place k knights on an n x n chessboard so none attack each other.
Uses backtracking to find a solution.
"""
from __future__ import annotations
import argparse
from typing import List, Tuple, Optional, Set

Position = Tuple[int, int]


def knight_attacks(a: Position, b: Position) -> bool:
    dr = abs(a[0] - b[0])
    dc = abs(a[1] - b[1])
    return (dr == 2 and dc == 1) or (dr == 1 and dc == 2)


def backtrack_knights(n: int, k: int) -> Optional[List[Position]]:
    # Backtracking to place k knights on n x n without conflicts
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


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Place k knights on an n x n board with no mutual attacks."
    )
    parser.add_argument("-n", type=int, default=5, help="board size (default: 5)")
    parser.add_argument("-k", type=int, default=5,
                        help="number of knights to place (default: 5)")
    args = parser.parse_args(argv)

    sol = backtrack_knights(args.n, args.k)
    if sol:
        print(f"Found placement for {args.k} knights on {args.n}x{args.n} board:")
        print(pretty_board(args.n, sol))
    else:
        print(f"No solution found for {args.k} knights on {args.n}x{args.n} board.")


if __name__ == "__main__":
    main()
