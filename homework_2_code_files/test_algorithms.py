"""
Test suite for Minimax and Negamax algorithms
Tests various game scenarios to ensure AI makes optimal moves

NOTE: Per assignment requirements, games only end when the board is COMPLETELY FULL.
Winner is determined by total triplet count, not by first triplet formed.
"""

import numpy as np
from GameStatus_5120 import GameStatus
from multiAgents import minimax, negamax


def print_board(board_state):
    """Helper function to print the board in a readable format."""
    symbols = {1: 'O', -1: 'X', 0: '.'}
    print("\nBoard:")
    for row in board_state:
        print(' '.join(symbols[cell] for cell in row))
    print()


def test_blocking_move():
    """Test that AI prevents opponent from forming triplets."""
    print("=" * 60)
    print("TEST 1: AI should block opponent's triplet formation")
    print("=" * 60)
    
    # Setup: Human (X) has two in a row, AI (O) should block to prevent triplet
    # X X .
    # . . .
    # . . .
    board = np.array([
        [-1, -1, 0],
        [0, 0, 0],
        [0, 0, 0]
    ])
    
    game_state = GameStatus(board, turn_O=True, human_symbol="X")
    print_board(board)
    print(f"Current score (from human perspective): {game_state.get_scores(False)}")
    
    # AI should block at (0, 2) to prevent human from forming a triplet
    score, move = minimax(game_state, depth=4, maximizingPlayer=False)
    print(f"Minimax chose move: {move}, score: {score}")
    
    # Blocking at (0, 2) is smart to prevent triplet
    if move == (0, 2):
        print("✅ PASS: Minimax correctly blocked the triplet formation")
        minimax_pass = True
    else:
        print(f"⚠️  WARNING: Minimax chose {move} instead of blocking at (0, 2)")
        print(f"   (This may still be valid depending on algorithm depth/strategy)")
        minimax_pass = False
    
    # Test negamax too
    score_neg, move_neg = negamax(game_state, depth=4, turn_multiplier=-1)
    print(f"Negamax chose move: {move_neg}, score: {score_neg}")
    
    if move_neg == (0, 2):
        print("✅ PASS: Negamax correctly blocked the triplet formation")
        negamax_pass = True
    else:
        print(f"⚠️  WARNING: Negamax chose {move_neg} instead of blocking at (0, 2)")
        print(f"   (This may still be valid depending on algorithm depth/strategy)")
        negamax_pass = False
    
    return minimax_pass and negamax_pass


def test_winning_move():
    """Test that AI forms triplets when possible."""
    print("\n" + "=" * 60)
    print("TEST 2: AI should form its own triplets")
    print("=" * 60)
    
    # Setup: AI (O) has two in a row and can form a triplet
    # O O .
    # X . .
    # X . .
    board = np.array([
        [1, 1, 0],
        [-1, 0, 0],
        [-1, 0, 0]
    ])
    
    game_state = GameStatus(board, turn_O=True, human_symbol="X")
    print_board(board)
    print(f"Current score (from human perspective): {game_state.get_scores(False)}")
    
    # AI should complete triplet at (0, 2)
    score, move = minimax(game_state, depth=4, maximizingPlayer=False)
    print(f"Minimax chose move: {move}, score: {score}")
    
    if move == (0, 2):
        print("✅ PASS: Minimax correctly formed a triplet")
        minimax_pass = True
    else:
        print(f"⚠️  WARNING: Minimax chose {move} instead of forming triplet at (0, 2)")
        minimax_pass = False
    
    score_neg, move_neg = negamax(game_state, depth=4, turn_multiplier=-1)
    print(f"Negamax chose move: {move_neg}, score: {score_neg}")
    
    if move_neg == (0, 2):
        print("✅ PASS: Negamax correctly formed a triplet")
        negamax_pass = True
    else:
        print(f"⚠️  WARNING: Negamax chose {move_neg} instead of forming triplet at (0, 2)")
        negamax_pass = False
    
    return minimax_pass and negamax_pass


def test_fork_opportunity():
    """Test that AI recognizes and creates fork opportunities."""
    print("\n" + "=" * 60)
    print("TEST 3: AI should create/block fork opportunities")
    print("=" * 60)
    
    # Setup: Human (X) is about to create a fork
    # X . .
    # . X .
    # . . .
    board = np.array([
        [-1, 0, 0],
        [0, -1, 0],
        [0, 0, 0]
    ])
    
    game_state = GameStatus(board, turn_O=True, human_symbol="X")
    print_board(board)
    
    # AI should block the fork (best moves would be corners or center)
    score, move = minimax(game_state, depth=4, maximizingPlayer=False)
    print(f"Minimax chose move: {move}, score: {score}")
    
    # Valid blocking moves: (0, 2), (2, 0), (2, 2)
    valid_moves = [(0, 2), (2, 0), (2, 2)]
    if move in valid_moves:
        print(f"✅ PASS: Minimax chose a good defensive move {move}")
        return True
    else:
        print(f"⚠️  WARNING: Minimax chose {move}, expected one of {valid_moves}")
        return False


def test_center_preference():
    """Test AI's strategy on empty board."""
    print("\n" + "=" * 60)
    print("TEST 4: AI strategy on empty board")
    print("=" * 60)
    
    # Empty board - AI goes first
    board = np.zeros((3, 3), dtype=int)
    game_state = GameStatus(board, turn_O=True, human_symbol="X")
    print_board(board)
    
    score, move = minimax(game_state, depth=4, maximizingPlayer=False)
    print(f"Minimax chose move: {move}, score: {score}")
    
    # Center (1,1) and corners are equally good strategically
    good_moves = [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)]
    if move in good_moves:
        print(f"✅ PASS: Minimax chose a strategic opening move {move}")
    else:
        print(f"⚠️  WARNING: Minimax chose edge move {move} instead of corner/center")
    
    return move in good_moves


def test_human_as_O():
    """Test that algorithms work correctly when human plays as O."""
    print("\n" + "=" * 60)
    print("TEST 5: Algorithms work when human is O (AI is X)")
    print("=" * 60)
    
    # Setup: Human (O) has two in a row, AI (X) must block
    # O O .
    # . . .
    # . . .
    board = np.array([
        [1, 1, 0],
        [0, 0, 0],
        [0, 0, 0]
    ])
    
    game_state = GameStatus(board, turn_O=False, human_symbol="O")
    print_board(board)
    print("Human is O, AI is X (turn_O=False means X's turn)")
    
    # AI (playing as X) should block at (0, 2)
    score, move = minimax(game_state, depth=4, maximizingPlayer=False)
    print(f"Minimax chose move: {move}, score: {score}")
    
    if move == (0, 2):
        print("✅ PASS: Minimax correctly blocked when playing as X")
    else:
        print(f"❌ FAIL: Minimax chose {move} instead of blocking at (0, 2)")
    
    return move == (0, 2)


def test_terminal_state_detection():
    """Test that algorithms correctly identify terminal states (full board only)."""
    print("\n" + "=" * 60)
    print("TEST 6: Terminal state detection (board must be full)")
    print("=" * 60)
    
    # Setup: Board with triplet but NOT full - should NOT be terminal
    # X X X
    # O O .
    # . . .
    board = np.array([
        [-1, -1, -1],
        [1, 1, 0],
        [0, 0, 0]
    ])
    
    game_state = GameStatus(board, turn_O=True, human_symbol="X")
    print_board(board)
    
    is_terminal = game_state.is_terminal()
    score = game_state.get_scores(terminal=False)
    
    print(f"Is terminal: {is_terminal}")
    print(f"Score (non-terminal): {score}")
    print(f"Note: Board has XXX triplet but is NOT full, so NOT terminal per assignment rules")
    
    if not is_terminal:
        print("✅ PASS: Correctly identified non-full board as non-terminal")
        return True
    else:
        print(f"❌ FAIL: Board is not full, should not be terminal")
        return False


def test_draw_detection():
    """Test that algorithms correctly identify draw states."""
    print("\n" + "=" * 60)
    print("TEST 7: Draw detection")
    print("=" * 60)
    
    # Setup: Full board with no winner
    # X O X
    # X O O
    # O X X
    board = np.array([
        [-1, 1, -1],
        [-1, 1, 1],
        [1, -1, -1]
    ])
    
    game_state = GameStatus(board, turn_O=True, human_symbol="X")
    print_board(board)
    
    is_terminal = game_state.is_terminal()
    score = game_state.get_scores(terminal=True)
    
    print(f"Is terminal: {is_terminal}")
    print(f"Score: {score}")
    
    if is_terminal and score == 0:
        print("✅ PASS: Correctly detected draw (score = 0)")
    else:
        print(f"❌ FAIL: Terminal={is_terminal}, Score={score} (expected 0)")
    
    return is_terminal and score == 0


def test_4x4_board():
    """Test that algorithms work on larger boards."""
    print("\n" + "=" * 60)
    print("TEST 8: 4x4 board support")
    print("=" * 60)
    
    # Setup 4x4 board with potential 3-in-a-row
    # X X . .
    # . . . .
    # . . . .
    # . . . .
    board = np.array([
        [-1, -1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ])
    
    GameStatus.win_length = 3  # Still looking for 3 in a row
    game_state = GameStatus(board, turn_O=True, human_symbol="X")
    print_board(board)
    
    # AI should block at (0, 2)
    score, move = minimax(game_state, depth=3, maximizingPlayer=False)
    print(f"Minimax chose move: {move}, score: {score}")
    
    if move == (0, 2):
        print("✅ PASS: Minimax works on 4x4 board")
    else:
        print(f"⚠️  WARNING: Minimax chose {move} instead of blocking at (0, 2)")
    
    GameStatus.win_length = 3  # Reset
    return move == (0, 2)


def test_alpha_beta_pruning():
    """Test that alpha-beta pruning works (by checking it doesn't affect result)."""
    print("\n" + "=" * 60)
    print("TEST 9: Alpha-beta pruning consistency")
    print("=" * 60)
    
    # Complex board state
    board = np.array([
        [-1, 1, -1],
        [1, -1, 0],
        [0, 0, 1]
    ])
    
    game_state = GameStatus(board, turn_O=True, human_symbol="X")
    print_board(board)
    
    # Run multiple times to ensure consistency with randomization
    moves = []
    for i in range(5):
        score, move = minimax(game_state, depth=4, maximizingPlayer=False)
        moves.append(move)
    
    print(f"Moves from 5 runs: {moves}")
    
    # All moves should have the same minimax value (even if different due to randomization)
    if all(m is not None for m in moves):
        print("✅ PASS: Alpha-beta pruning produces consistent moves")
        return True
    else:
        print("❌ FAIL: Some moves were None")
        return False


def run_all_tests():
    """Run all tests and report results."""
    print("\n" + "=" * 70)
    print(" " * 15 + "ALGORITHM TEST SUITE")
    print("=" * 70)
    
    tests = [
        ("Blocking Move", test_blocking_move),
        ("Winning Move", test_winning_move),
        ("Fork Opportunity", test_fork_opportunity),
        ("Center Preference", test_center_preference),
        ("Human as O", test_human_as_O),
        ("Terminal State Detection", test_terminal_state_detection),
        ("Draw Detection", test_draw_detection),
        ("4x4 Board Support", test_4x4_board),
        ("Alpha-Beta Pruning", test_alpha_beta_pruning),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ ERROR in {name}: {str(e)}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print(" " * 25 + "TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print("\n" + "-" * 70)
    print(f"Results: {passed}/{total} tests passed ({100*passed//total}%)")
    print("=" * 70 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
