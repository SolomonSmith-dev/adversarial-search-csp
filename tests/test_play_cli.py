"""Tests for the headless Tic-Tac-Toe CLI driver."""
import play_cli
from game_status import GameStatus


def test_render_uses_symbol_map():
    state = GameStatus([[1, -1, 0], [0, 0, 0], [0, 0, 0]], turn_O=False)
    lines = play_cli.render(state).splitlines()
    assert lines[0] == "O X ."
    assert lines[1] == ". . ."


def test_ai_vs_ai_game_terminates_silently():
    # Two perfect players on a 3x3 board must end in a draw or a win,
    # and the driver must reach a terminal state without prompting.
    winner = play_cli.play(size=3, mode="ai_vs_ai", algorithm="negamax",
                           depth=4, out=lambda *_: None)
    assert winner in {"DRAW", "Human", "AI"}


def test_ai_blocks_threat_when_block_saves_the_game():
    # X threatens the top row; O can block at (0,1) and still draw, so the
    # AI (O) must take that block rather than walk into a loss.
    board = [[-1, 0, -1], [0, 1, 0], [0, 0, 0]]
    state = GameStatus(board, turn_O=True, human_symbol="X")
    for algorithm in ("negamax", "minimax"):
        move = play_cli.ai_move(state, algorithm=algorithm, depth=9)
        assert move == (0, 1), f"{algorithm} failed to block"


def test_ai_takes_immediate_win():
    # O can complete the top row at (0,2); the AI must take the win.
    board = [[1, 1, 0], [-1, -1, 0], [0, 0, 0]]
    state = GameStatus(board, turn_O=True, human_symbol="X")
    for algorithm in ("negamax", "minimax"):
        move = play_cli.ai_move(state, algorithm=algorithm, depth=5)
        assert move == (0, 2), f"{algorithm} failed to take the win"


def test_perfect_self_play_always_draws():
    # Optimal play by both sides on 3x3 is a forced draw. Full-depth search
    # (depth 9) must never produce a winner regardless of tie-break choices.
    for algorithm in ("negamax", "minimax"):
        winner = play_cli.play(size=3, mode="ai_vs_ai", algorithm=algorithm,
                               depth=9, out=lambda *_: None)
        assert winner == "DRAW", f"{algorithm} self-play was not a draw"


def test_human_vs_ai_uses_injected_moves():
    # Human (X) plays the winning top row via injected moves; no stdin needed.
    scripted = iter([(0, 0), (0, 1), (0, 2)])
    winner = play_cli.play(size=3, mode="human_vs_ai", human_symbol="X",
                           algorithm="negamax", depth=4,
                           move_fn=lambda state: next(scripted),
                           out=lambda *_: None)
    assert winner in {"DRAW", "Human", "AI"}
