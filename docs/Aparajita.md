Aparajita — Testing & Quality Assurance Lead

Files / Areas:
	•	tests/ folder (she owns everything inside it)
	•	Helps debug and confirm all major modules (multiAgents.py, GameStatus_5120.py, large_board_tic_tac_toe.py) work together
	•	Verifies that AI, board logic, and GUI all follow the assignment’s rules

---

Your Mission

You are the tester and debugger of the project.
Your main job is to make sure:
	1.	Every file works correctly on its own.
	2.	Everything connects properly (AI ↔ Game ↔ GUI).
	3.	We can prove to the professor that our code works through screenshots, test logs, and stable results.

Think of yourself as the quality control engineer.
When you sign off, we should be 100% confident that nothing crashes or gives wrong results.

⸻

```markdown
Aparajita — Testing & Quality Assurance Lead

Files / Areas:
	- tests/ folder (she owns everything inside it)
	- Helps debug and confirm all major modules (multiAgents.py, GameStatus_5120.py, large_board_tic_tac_toe.py) work together
	- Verifies that AI, board logic, and GUI all follow the assignment’s rules

---

Your Mission

You are the tester and debugger of the project.
Your main job is to make sure:
	1. Every file works correctly on its own.
	2. Everything connects properly (AI ↔ Game ↔ GUI).
	3. We can prove to the professor that our code works through screenshots, test logs, and stable results.

Think of yourself as the quality control engineer.
When you sign off, we should be 100% confident that nothing crashes or gives wrong results.

---

What You’ll Do

You’ll write Python test scripts (using pytest) that automatically check if:
	- The AI plays valid moves.
	- The board correctly updates.
	- Wins, losses, and draws are detected correctly.
	- The GUI runs without crashes.
	- The whole system can handle different board sizes (3×3, 4×4, 5×5).

---

Folder Setup

You’ll create a folder called:

tests/

Inside it, you’ll make small files like:

tests/test_game_logic.py
tests/test_ai_algorithms.py
tests/test_integration.py

Each file will contain short test functions that call Alex’s and Solomon’s code.

Example structure:

```python
from GameStatus_5120 import GameState

def test_legal_moves():
		s = GameState(empty_3x3, 1, 3)
		moves = s.get_legal_moves()
		assert len(moves) == 9
```

---

What to Test (Checklist)

1. Game Logic (Alex’s part)

You’ll test:
	- get_legal_moves() returns the right number of moves.
	- get_new_state() correctly changes the board and flips the turn.
	- ai_won() and opponent_won() detect wins in all directions.
	- is_draw() correctly detects full boards with no winner.
	- get_scores() returns numbers (not errors).

You can test both small and big boards:
	- 3×3 = normal Tic-Tac-Toe
	- 4×4 and 5×5 = larger versions

---

2. AI Algorithms (Solomon’s part)

You’ll test:
	- minimax and alphabeta give the same results on small boards.
	- negamax matches the same result.
	- AI always returns legal moves (no out-of-range or occupied squares).
	- AI never crashes on 3×3, 4×4, 5×5 boards.
	- Run-time checks: 3×3 = instant, 4×4 = under 5 seconds, 5×5 = playable.

You’ll use simple assertions like:

```python
from multiAgents import choose_ai_move
move = choose_ai_move(some_state, depth=3)
assert move in some_state.get_legal_moves()
```

---

3. Integration (AI ↔ GUI ↔ Board)

You’ll test that:
	- Human and AI alternate correctly.
	- Game ends properly after a win or draw.
	- GUI updates state visually (you can run it manually to confirm).
	- Pressing "R" resets the board.
	- Pressing "1", "2", or "3" changes depth in the HUD (you’ll visually confirm).

You don’t have to automate GUI tests, but you’ll make sure manual tests work:
	1. Run the GUI.
	2. Play a few turns.
	3. Take screenshots of:
		- Start screen
		- Mid-game
		- End state (win/draw)

---

4. Error Handling

You’ll make sure the game doesn’t crash when:
	- You click an already-filled cell.
	- You press keys too quickly.
	- The AI has no moves left.
	- The board size changes.

You’ll record what happens and let Alex and Solomon know if you find any bugs.

---

How You’ll Know You’re Done
	- You can run all tests with:

		pytest -q

	- Everything passes (no red error text).
	- You can play through a full game in the GUI without crashes.
	- You have 3–4 clean screenshots of the GUI in action.
	- The professor’s rubric items (correctness, runtime, documentation, readability) are covered by your checks.
	- Everyone else has confirmed your tests helped them fix bugs.

---

What You Need from Everyone

From	What You Need	Why
Solomon	A working choose_ai_move() function and Minimax / AlphaBeta logic	So you can test if AI makes valid moves and wins/draws correctly
Alex	The finished GameState class and GUI setup	So you can test if the rules, moves, and rendering work properly
Lyssa	Final report outline	To make sure all screenshots and results you verify match the report

That’s because:
	- She needs the GameState methods to exist before she can test them.
	- She needs the AI to return moves to test correctness.
	- The GUI can come slightly later — she’ll still be able to run logic tests first.

So, can begin as soon as:
	- Alex’s get_legal_moves(), get_new_state(), is_terminal(), and get_scores() are working.
	- Solomon’s choose_ai_move() runs on a 3×3 board without crashing.

So roughly:
	- Start testing once game logic + AI are connected
	- Finish when everything passes and screenshots are captured (a few days before submission)

---

Deliverables

File	Description
tests/test_game_logic.py	Unit tests for Alex’s board logic
tests/test_ai_algorithms.py	Tests for Solomon’s Minimax, Alpha-Beta, Negamax
tests/test_integration.py	Small tests that simulate full game turns
Manual test report	Notes or screenshots proving GUI and AI integration works
Screenshots	For Lyssa’s report (start, mid, end states)

---

Quick Summary for Aparajita
	- You are the tester, not the builder.
	- You’ll make sure everything runs, connects, and plays correctly.
	- You’ll run and write tests using pytest.
	- You’ll collect screenshots and short notes for proof.
	- You’ll help confirm that the project is 100% stable before we zip and submit.

---
```