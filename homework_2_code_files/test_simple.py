"""
Simple Test Suite for Minimax and Negamax
Tests based on assignment requirements:
- Games only end when board is COMPLETELY FULL
- Winner determined by TOTAL TRIPLET COUNT
"""

import numpy as np
from GameStatus_5120 import GameStatus
from multiAgents import minimax, negamax


def print_board(board_state):
    """Helper function to print the board."""
    symbols = {1: 'O', -1: 'X', 0: '.'}
    for row in board_state:
        print(' '.join(symbols[cell] for cell in row))
    print()


def test_terminal_only_when_full():
    """Test 1: Board is terminal ONLY when completely full."""
    print("=" * 60)
    print("TEST 1: Terminal State - Board Must Be Full")
    print("=" * 60)
    
    # Board with triplet but NOT full - should NOT be terminal
    board1 = np.array([
        [-1, -1, -1],  # XXX - triplet!
        [1, 1, 0],
        [0, 0, 0]
    ])
    game1 = GameStatus(board1, turn_O=True, human_symbol="X")
    print("Board with XXX triplet but not full:")
    print_board(board1)
    print(f"Is terminal? {game1.is_terminal()} (should be False)")
    assert not game1.is_terminal(), "❌ FAIL: Non-full board marked as terminal!"
    print("✅ PASS: Non-full board correctly NOT terminal\n")
    
    # Full board - should BE terminal
    board2 = np.array([
        [-1, 1, -1],
        [-1, 1, 1],
        [1, -1, -1]
    ])
    game2 = GameStatus(board2, turn_O=True, human_symbol="X")
    print("Full board:")
    print_board(board2)
    print(f"Is terminal? {game2.is_terminal()} (should be True)")
    assert game2.is_terminal(), "❌ FAIL: Full board not marked as terminal!"
    print("✅ PASS: Full board correctly IS terminal\n")
    
    return True


def test_triplet_counting():
    """Test 2: Score based on triplet count, not single win."""
    print("=" * 60)
    print("TEST 2: Winner Determined by Total Triplet Count")
    print("=" * 60)
    
    # Full board where X has more triplets than O
    # Row 0: XXX (X triplet)
    # Row 2: XXX (X triplet)
    # Col 1: XOX (no triplet)
    # O has no triplets
    board = np.array([
        [-1, -1, -1],  # XXX - 1 horizontal triplet for X
        [1, 1, -1],    # OOX
        [-1, -1, -1]   # XXX - 1 horizontal triplet for X
    ])
    
    game = GameStatus(board, turn_O=True, human_symbol="X")
    print("Full board with multiple triplets:")
    print_board(board)
    
    score = game.get_scores(terminal=True)
    print(f"Score: {score}")
    print(f"Interpretation: score > 0 means Human (X) wins")
    print(f"                score < 0 means AI (O) wins")
    print(f"                score = 0 means Draw")
    print(f"Expected: X has 2 triplets (rows 0 and 2), O has 0 triplets")
    
    # X is human, should have positive score if X has more triplets
    if score > 0:
        print("✅ PASS: Correctly counted multiple triplets\n")
        return True
    else:
        print(f"❌ FAIL: Score should be positive but got {score}\n")
        return False


def test_minimax_basic():
    """Test 3: Minimax produces valid moves."""
    print("=" * 60)
    print("TEST 3: Minimax Produces Valid Moves")
    print("=" * 60)
    
    # Simple non-full board
    board = np.array([
        [-1, 1, 0],
        [0, -1, 0],
        [1, 0, 0]
    ])
    game = GameStatus(board, turn_O=True, human_symbol="X")
    print("Board state:")
    print_board(board)
    
    # AI (O) turn - minimizing player
    score, move = minimax(game, depth=3, maximizingPlayer=False)
    print(f"Minimax (AI/O) chose: {move}, score: {score}")
    
    valid_moves = game.get_moves()
    print(f"Valid moves: {valid_moves}")
    
    if move in valid_moves:
        print("✅ PASS: Minimax returned valid move\n")
        return True
    else:
        print("❌ FAIL: Minimax returned invalid move\n")
        return False


def test_negamax_basic():
    """Test 4: Negamax produces valid moves."""
    print("=" * 60)
    print("TEST 4: Negamax Produces Valid Moves")
    print("=" * 60)
    
    board = np.array([
        [-1, 1, 0],
        [0, -1, 0],
        [1, 0, 0]
    ])
    game = GameStatus(board, turn_O=True, human_symbol="X")
    print("Board state:")
    print_board(board)
    
    # AI (O) turn - turn_multiplier = -1 for AI
    score, move = negamax(game, depth=3, turn_multiplier=-1)
    print(f"Negamax (AI/O) chose: {move}, score: {score}")
    
    valid_moves = game.get_moves()
    print(f"Valid moves: {valid_moves}")
    
    if move in valid_moves:
        print("✅ PASS: Negamax returned valid move\n")
        return True
    else:
        print("❌ FAIL: Negamax returned invalid move\n")
        return False


def test_draw_detection():
    """Test 5: Correctly detect draws (full board, equal triplets)."""
    print("=" * 60)
    print("TEST 5: Draw Detection")
    print("=" * 60)
    
    # Full board with equal triplets
    board = np.array([
        [-1, 1, -1],
        [-1, 1, 1],
        [1, -1, -1]
    ])
    game = GameStatus(board, turn_O=True, human_symbol="X")
    print("Full board:")
    print_board(board)
    
    is_terminal = game.is_terminal()
    score = game.get_scores(terminal=True)
    
    print(f"Is terminal? {is_terminal}")
    print(f"Score: {score}")
    
    if is_terminal and score == 0:
        print("✅ PASS: Correctly detected draw\n")
        return True
    else:
        print(f"❌ FAIL: Terminal={is_terminal}, Score={score}\n")
        return False


def test_4x4_board():
    """Test 6: Algorithm works on 4x4 board."""
    print("=" * 60)
    print("TEST 6: 4x4 Board Support")
    print("=" * 60)
    
    board = np.array([
        [-1, -1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ])
    game = GameStatus(board, turn_O=True, human_symbol="X")
    print("4x4 board:")
    print_board(board)
    
    try:
        score, move = minimax(game, depth=3, maximizingPlayer=False)
        print(f"Minimax chose: {move}, score: {score}")
        
        if move in game.get_moves():
            print("✅ PASS: Works on 4x4 board\n")
            return True
        else:
            print("❌ FAIL: Invalid move on 4x4 board\n")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception on 4x4 board: {e}\n")
        return False


def test_5x5_board():
    """Test 7: Algorithm works on 5x5 board."""
    print("=" * 60)
    print("TEST 7: 5x5 Board Support")
    print("=" * 60)
    
    board = np.zeros((5, 5), dtype=int)
    board[0][0] = -1
    board[0][1] = -1
    
    game = GameStatus(board, turn_O=True, human_symbol="X")
    print("5x5 board:")
    print_board(board)
    
    try:
        score, move = minimax(game, depth=2, maximizingPlayer=False)
        print(f"Minimax chose: {move}, score: {score}")
        
        if move in game.get_moves():
            print("✅ PASS: Works on 5x5 board\n")
            return True
        else:
            print("❌ FAIL: Invalid move on 5x5 board\n")
            return False
    except Exception as e:
        print(f"❌ FAIL: Exception on 5x5 board: {e}\n")
        return False


def test_human_symbol_tracking():
    """Test 8: Human symbol (X or O) is correctly tracked."""
    print("=" * 60)
    print("TEST 8: Human Symbol Tracking")
    print("=" * 60)
    
    # Test with human as X
    board1 = np.array([
        [-1, -1, -1],
        [1, 1, 0],
        [0, 0, 0]
    ])
    game1 = GameStatus(board1, turn_O=True, human_symbol="X")
    score1 = game1.get_scores(terminal=False)
    print(f"Human is X, board has XXX triplet")
    print(f"Score: {score1} (should be positive for human advantage)")
    
    # Test with human as O
    board2 = np.array([
        [1, 1, 1],
        [-1, -1, 0],
        [0, 0, 0]
    ])
    game2 = GameStatus(board2, turn_O=True, human_symbol="O")
    score2 = game2.get_scores(terminal=False)
    print(f"Human is O, board has OOO triplet")
    print(f"Score: {score2} (should be positive for human advantage)")
    
    if score1 > 0 and score2 > 0:
        print("✅ PASS: Human symbol correctly tracked\n")
        return True
    else:
        print(f"❌ FAIL: Scores incorrect - X:{score1}, O:{score2}\n")
        return False


def run_all_tests():
    """Run all tests and report results."""
    print("\n" + "=" * 60)
    print("       SIMPLE TEST SUITE - ASSIGNMENT REQUIREMENTS")
    print("=" * 60 + "\n")
    
    tests = [
        ("Terminal Only When Full", test_terminal_only_when_full),
        ("Triplet Counting", test_triplet_counting),
        ("Minimax Basic", test_minimax_basic),
        ("Negamax Basic", test_negamax_basic),
        ("Draw Detection", test_draw_detection),
        ("4x4 Board Support", test_4x4_board),
        ("5x5 Board Support", test_5x5_board),
        ("Human Symbol Tracking", test_human_symbol_tracking),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"❌ ERROR in {name}: {e}\n")
            results.append((name, False))
    
    # Print summary
    print("=" * 60)
    print("                    TEST SUMMARY")
    print("=" * 60)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
    
    print("-" * 60)
    print(f"Results: {passed_count}/{total_count} tests passed ({100*passed_count//total_count}%)")
    print("=" * 60 + "\n")
    
    return passed_count == total_count


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
