"""Tests for the CSP solvers."""
from knights_csp import backtrack_knights, knight_attacks
from vehicles_csp import REQUIRED_STOPS
from vehicles_csp import solve as vehicles_solve


def test_knights_solution_has_correct_count():
    sol = backtrack_knights(n=5, k=5)
    assert sol is not None
    assert len(sol) == 5


def test_knights_solution_has_no_attacks():
    sol = backtrack_knights(n=5, k=5)
    assert sol is not None
    for i, a in enumerate(sol):
        for b in sol[i + 1:]:
            assert not knight_attacks(a, b), f"Knights at {a} and {b} attack each other"


def test_knights_solution_positions_within_board():
    n = 5
    sol = backtrack_knights(n=n, k=5)
    assert sol is not None
    for r, c in sol:
        assert 0 <= r < n
        assert 0 <= c < n


def test_vehicles_solution_exists():
    sol = vehicles_solve()
    assert sol is not None
    assert set(sol.keys()) == {"A", "B", "C", "D", "E"}


def test_vehicles_unary_constraints():
    sol = vehicles_solve()
    assert sol is not None
    assert sol["B"][0] == 1
    assert sol["B"][2] == "arrive"
    assert sol["D"][0] >= 3
    assert sol["A"][0] <= 2


def test_vehicles_required_stops():
    sol = vehicles_solve()
    assert sol is not None
    for v, (t, s, a) in sol.items():
        assert s == REQUIRED_STOPS[v]


def test_vehicles_no_two_at_same_time_and_stop():
    sol = vehicles_solve()
    assert sol is not None
    seen = set()
    for v, (t, s, a) in sol.items():
        key = (t, s)
        assert key not in seen, f"Two vehicles at {key}"
        seen.add(key)


def test_vehicles_d_arrives_before_c_leaves_when_applicable():
    sol = vehicles_solve()
    assert sol is not None
    tD, _, aD = sol["D"]
    tC, _, aC = sol["C"]
    if aD == "arrive" and aC == "leave":
        assert tD < tC
