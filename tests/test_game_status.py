"""Tests for the GameStatus class."""
from GameStatus_5120 import GameStatus


def empty_board(n=3):
    return [[0] * n for _ in range(n)]


def test_get_moves_empty_board_returns_all_cells():
    state = GameStatus(empty_board(3), turn_O=True)
    assert len(state.get_moves()) == 9


def test_get_moves_excludes_filled_cells():
    board = empty_board(3)
    board[1][1] = 1
    state = GameStatus(board, turn_O=False)
    moves = state.get_moves()
    assert (1, 1) not in moves
    assert len(moves) == 8


def test_is_terminal_empty_board_is_false():
    state = GameStatus(empty_board(3), turn_O=True)
    assert state.is_terminal() is False


def test_is_terminal_horizontal_win_is_true():
    board = [[-1, -1, -1], [0, 0, 0], [0, 0, 0]]
    state = GameStatus(board, turn_O=True)
    assert state.is_terminal() is True


def test_is_terminal_vertical_win_is_true():
    board = [[1, 0, 0], [1, 0, 0], [1, 0, 0]]
    state = GameStatus(board, turn_O=False)
    assert state.is_terminal() is True


def test_is_terminal_diagonal_win_is_true():
    board = [[-1, 0, 0], [0, -1, 0], [0, 0, -1]]
    state = GameStatus(board, turn_O=True)
    assert state.is_terminal() is True


def test_is_terminal_full_board_no_winner_is_draw():
    board = [[1, -1, 1], [-1, 1, -1], [-1, 1, -1]]
    state = GameStatus(board, turn_O=True)
    assert state.is_terminal() is True
    assert state.winner == "DRAW"


def test_get_new_state_does_not_mutate_original():
    board = empty_board(3)
    state = GameStatus(board, turn_O=False)
    new_state = state.get_new_state((0, 0))
    assert state.board_state[0][0] == 0
    assert new_state.board_state[0][0] == -1


def test_get_new_state_toggles_turn():
    state = GameStatus(empty_board(3), turn_O=True)
    new_state = state.get_new_state((1, 1))
    assert state.turn_O is True
    assert new_state.turn_O is False
