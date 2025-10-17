"""Quick debug to see what minimax returns on empty board."""

from GameStatus_5120 import GameStatus
from multiAgents import minimax

# Create empty 3x3 board
board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
game = GameStatus(board, turn_O=True, human_symbol="X")

print("Board:", game.board_state)
print("Is terminal:", game.is_terminal())
print("Valid moves:", game.get_moves())

# Try minimax
print("\nCalling minimax with depth=2, maximizing_player=False")
result = minimax(game, depth=2, maximizing_player=False)
print(f"Result: {result}")
print(f"Type of move: {type(result[1])}")
print(f"Move value: {result[1]}")

if result[1] is not None:
    print(f"Move is tuple: {isinstance(result[1], tuple)}")
    print(f"Move subscriptable: {hasattr(result[1], '__getitem__')}")
