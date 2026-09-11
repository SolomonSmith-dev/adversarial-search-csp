"""The game-agnostic search drives both games from one implementation.

These tests are the proof that ``games/search.py`` knows nothing game-specific:
the identical ``negamax`` picks correct Tic-Tac-Toe moves (through the adapter)
and correct Connect Four moves.
"""
from connect_four import ConnectFour
from game_status import GameStatus
from search import negamax
from tictactoe_adapter import TicTacToeState


def test_generic_search_blocks_in_tic_tac_toe():
    # X . X / . O . / . . .  -> O must block the top row at (0, 1).
    gs = GameStatus([[-1, 0, -1], [0, 1, 0], [0, 0, 0]],
                    turn_O=True, human_symbol="X")
    _, move = negamax(TicTacToeState(gs), depth=9)
    assert move == (0, 1)


def test_generic_search_takes_tic_tac_toe_win():
    # O O . / X X . / . . .  -> O completes the top row at (0, 2).
    gs = GameStatus([[1, 1, 0], [-1, -1, 0], [0, 0, 0]],
                    turn_O=True, human_symbol="X")
    _, move = negamax(TicTacToeState(gs), depth=5)
    assert move == (0, 2)


def test_generic_search_wins_connect_four():
    # X across cols 0-2 on the bottom; X to move should complete at col 3.
    state = ConnectFour()
    for c in [0, 0, 1, 1, 2, 2]:
        state = state.make_move(c)
    _, move = negamax(state, depth=4)
    assert move == 3


def test_same_search_object_handles_both_state_types():
    # One function, two unrelated state classes, both returning a legal move.
    ttt = TicTacToeState(GameStatus([[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                                    turn_O=False, human_symbol="X"))
    c4 = ConnectFour()
    _, ttt_move = negamax(ttt, depth=2)
    _, c4_move = negamax(c4, depth=2)
    assert ttt_move in ttt.legal_moves()
    assert c4_move in c4.legal_moves()
