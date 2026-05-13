"""Tests for minimax and negamax."""
from game_status import GameStatus
from multiAgents import minimax, negamax, ordered_moves


def test_minimax_terminal_returns_score_and_no_move():
    board = [[-1, -1, -1], [1, 1, 0], [1, 0, 0]]
    state = GameStatus(board, turn_O=True)
    score, move = minimax(state, depth=3, maximizing_player=True)
    assert move is None
    assert score == 1000


def test_minimax_picks_winning_move_for_x():
    board = [[-1, -1, 0], [0, 0, 0], [0, 0, 0]]
    state = GameStatus(board, turn_O=False, human_symbol="X")
    score, move = minimax(state, depth=1, maximizing_player=True)
    assert move == (0, 2)
    assert score == 1000


def test_negamax_picks_winning_move():
    board = [[-1, -1, 0], [0, 0, 0], [0, 0, 0]]
    state = GameStatus(board, turn_O=False, human_symbol="X")
    _, move = negamax(state, depth=1)
    assert move == (0, 2)


def test_ordered_moves_surfaces_winning_move_first():
    board = [[-1, -1, 0], [0, 0, 0], [0, 0, 0]]
    state = GameStatus(board, turn_O=False, human_symbol="X")
    moves = ordered_moves(state)
    assert moves[0] == (0, 2)
