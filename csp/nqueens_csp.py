"""
Place N queens on an N x N board so none attack each other, solved with the
generic CSP framework (MRV + forward checking).

Formulation: one variable per column (0..N-1). A variable's value is the row of
the queen in that column, so no two queens ever share a column by construction.
The single pairwise constraint forbids two queens on the same row or diagonal.

Examples:
    python3 csp/nqueens_csp.py           # 8 queens
    python3 csp/nqueens_csp.py -n 12
    python3 csp/nqueens_csp.py -n 8 --no-forward-checking --no-mrv  # naive
"""
from __future__ import annotations

import argparse
from typing import Dict, List, Optional

from backtracking import CSP, Constraint, SearchStats, backtracking_search


class QueensConstraint(Constraint[int, int]):
    """Two queens (columns c1, c2) must not share a row or a diagonal."""

    def __init__(self, c1: int, c2: int):
        super().__init__([c1, c2])
        self.c1 = c1
        self.c2 = c2

    def satisfied(self, assignment: Dict[int, int]) -> bool:
        if self.c1 not in assignment or self.c2 not in assignment:
            return True  # defer until both columns have a row
        r1, r2 = assignment[self.c1], assignment[self.c2]
        if r1 == r2:
            return False  # same row
        return abs(r1 - r2) != abs(self.c1 - self.c2)  # same diagonal


def build_csp(n: int) -> CSP[int, int]:
    columns = list(range(n))
    domains = {c: list(range(n)) for c in columns}
    csp: CSP[int, int] = CSP(columns, domains)
    for c1 in columns:
        for c2 in range(c1 + 1, n):
            csp.add_constraint(QueensConstraint(c1, c2))
    return csp


def solve(n: int, use_mrv: bool = True, use_forward_checking: bool = True):
    """Return (solution, stats). Solution maps column -> row, or None."""
    return backtracking_search(build_csp(n), use_mrv=use_mrv,
                               use_forward_checking=use_forward_checking)


def pretty_board(n: int, solution: Dict[int, int]) -> str:
    rows = []
    for r in range(n):
        cells = ["Q" if solution.get(c) == r else "." for c in range(n)]
        rows.append(" ".join(cells))
    return "\n".join(rows)


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(
        description="Solve the N-Queens problem with the generic CSP framework."
    )
    parser.add_argument("-n", type=int, default=8, help="board size (default: 8)")
    parser.add_argument("--no-mrv", action="store_true",
                        help="disable minimum-remaining-values ordering")
    parser.add_argument("--no-forward-checking", action="store_true",
                        help="disable forward checking")
    args = parser.parse_args(argv)

    solution, stats = solve(args.n, use_mrv=not args.no_mrv,
                            use_forward_checking=not args.no_forward_checking)
    if solution is None:
        print(f"No solution for {args.n} queens.  [{stats}]")
        return
    print(f"Solution for {args.n} queens:")
    print(pretty_board(args.n, solution))
    print(f"[{stats}]")


if __name__ == "__main__":
    main()
