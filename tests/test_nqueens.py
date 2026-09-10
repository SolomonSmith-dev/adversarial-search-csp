"""Tests for the generic CSP framework via the N-Queens solver."""
import pytest

from nqueens_csp import QueensConstraint, solve


def _no_attacks(solution):
    """True if no two queens in the column->row solution attack each other."""
    cols = sorted(solution)
    for i, c1 in enumerate(cols):
        for c2 in cols[i + 1:]:
            r1, r2 = solution[c1], solution[c2]
            if r1 == r2:
                return False
            if abs(r1 - r2) == abs(c1 - c2):
                return False
    return True


@pytest.mark.parametrize("n", [1, 4, 5, 8, 10])
def test_solution_is_valid(n):
    solution, _ = solve(n)
    assert solution is not None
    assert set(solution.keys()) == set(range(n))
    assert all(0 <= r < n for r in solution.values())
    assert _no_attacks(solution)


@pytest.mark.parametrize("n", [2, 3])
def test_unsatisfiable_instances_return_none(n):
    solution, _ = solve(n)
    assert solution is None


def test_forward_checking_reduces_search():
    # Forward checking must explore no more nodes than naive backtracking,
    # and on 8-queens it explores strictly fewer.
    _, naive = solve(8, use_mrv=False, use_forward_checking=False)
    _, fc = solve(8, use_mrv=False, use_forward_checking=True)
    assert fc.nodes < naive.nodes
    assert naive.prunings == 0 and fc.prunings > 0


def test_mrv_and_forward_checking_together_solve_larger_board():
    solution, stats = solve(12, use_mrv=True, use_forward_checking=True)
    assert solution is not None
    assert _no_attacks(solution)
    assert stats.nodes > 0


def test_queens_constraint_defers_until_both_assigned():
    c = QueensConstraint(0, 3)
    assert c.satisfied({0: 1}) is True          # c2 unassigned -> defer
    assert c.satisfied({0: 1, 3: 1}) is False   # same row
    assert c.satisfied({0: 0, 3: 3}) is False   # same diagonal
    assert c.satisfied({0: 0, 3: 2}) is True     # safe
