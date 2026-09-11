"""Tests for Connect Four and the game-agnostic negamax search."""
import pytest

from connect_four import ConnectFour
from search import SearchStats, negamax


def drop(state, cols):
    """Play a sequence of columns and return the resulting state."""
    for c in cols:
        state = state.make_move(c)
    return state


def test_gravity_stacks_pieces_from_the_bottom():
    state = ConnectFour().make_move(3)
    assert state.board[-1][3] == 1          # bottom row filled first
    assert state.board[0][3] == 0           # top still empty
    state = state.make_move(3)
    assert state.board[-2][3] == -1         # second piece rests on the first


def test_full_column_is_illegal():
    state = ConnectFour(rows=6, cols=7)
    state = drop(state, [0] * 6)            # fill column 0
    assert 0 not in state.legal_moves()
    with pytest.raises(ValueError):
        state.make_move(0)


def test_horizontal_vertical_and_diagonal_wins_detected():
    # Horizontal: X across the bottom row.
    horiz = drop(ConnectFour(), [0, 0, 1, 1, 2, 2, 3])
    assert horiz.winner == "X"
    assert horiz.is_terminal()

    # Vertical: X stacks four in column 0.
    vert = drop(ConnectFour(), [0, 1, 0, 1, 0, 1, 0])
    assert vert.winner == "X"

    # Diagonal (up-right): a staircase of X.
    diag = drop(ConnectFour(), [0, 1, 1, 2, 2, 3, 2, 3, 3, 6, 3])
    assert diag.winner == "X"


def test_empty_board_is_not_terminal_and_scores_zero_ish():
    state = ConnectFour()
    assert not state.is_terminal()
    assert state.winner is None
    assert state.score() == 0  # symmetric empty board


def test_ai_takes_immediate_win():
    # X has three across the bottom (cols 0-2); X to move must play col 3.
    state = drop(ConnectFour(), [0, 0, 1, 1, 2, 2])
    value, move = negamax(state, depth=4)
    assert move == 3
    assert value > 0


def test_ai_blocks_immediate_loss():
    # X threatens cols 0-2 on the bottom; O to move must block col 3.
    state = drop(ConnectFour(), [0, 6, 1, 5, 2])
    assert state.current_player == -1       # O to move
    _, move = negamax(state, depth=4)
    assert move == 3


def test_center_ordering_puts_middle_column_first():
    order = ConnectFour(cols=7).order_moves()
    assert order[0] == 3                     # center column
    assert set(order) == set(range(7))


def test_search_stats_counts_nodes():
    stats = SearchStats()
    negamax(ConnectFour(), depth=4, stats=stats)
    assert stats.nodes > 1


def test_draw_on_a_tiny_unwinnable_board():
    # A 2-wide board needing 4-in-a-row cannot be won; filling it draws.
    state = ConnectFour(rows=2, cols=2, connect=4)
    state = drop(state, [0, 1, 0, 1])       # board full, no line possible
    assert state.is_terminal()
    assert state.winner == "DRAW"
    assert state.score() == 0
