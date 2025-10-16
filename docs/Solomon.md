Here is my portion

Absolutely — here’s your section (Solomon’s) again, cleaned up, simplified, and formatted in Markdown for your team workspace.
It matches the style of Alex, Aparajita, and Lyssa’s sections — easy to read, clear expectations, and ready to paste into Notion or your README.

---

Solomon — AI Algorithms & Integration Lead

File: multiAgents.py

---

Mission

You are the AI developer for this project.
Your job is to make the computer think strategically using Minimax, Alpha-Beta Pruning, and Negamax algorithms.
Your work makes the AI opponent capable of playing against a human intelligently on any board size (3×3, 4×4, or 5×5).

You are building the brain of the game — everything that decides what the AI should do next.

---

Responsibilities

Task	Description
AI Decision System	Implement Minimax, Alpha-Beta, and Negamax algorithms that explore possible moves and choose the best one.
Evaluation Function	Design a scoring system that judges how good each position is.
Integration	Provide one main entry function (choose_ai_move) that Alex’s GUI can call.
Optimization	Make the AI fast and efficient using pruning and move ordering.
Collaboration	Work closely with Alex (who builds the board + GUI) and Aparajita (who tests your algorithms).


---

Core Functions You’ll Write

Function	What It Does
choose_ai_move(state, depth, algo)	Main entry point. Takes the current game state and returns the AI’s chosen move.
minimax(state, depth, maximizing)	Basic algorithm that explores all moves and picks the best one.
alphabeta(state, depth, alpha, beta, maximizing)	Faster version of Minimax that skips unnecessary branches.
negamax(state, depth, alpha, beta, color)	Simplified version of Minimax that uses symmetry and sign flipping.

Each one should handle any board size — not just 3×3.

---

How the AI Sees the Game

When it’s the AI’s turn:
	1.	It looks at all legal moves (get_legal_moves()).
	2.	It simulates each move by generating a new game state (get_new_state(move)).
	3.	It checks whether the game has ended (is_terminal()).
	4.	It evaluates how good that position is (get_scores()).
	5.	It picks the move that gives the best final result after looking several moves ahead.

You’ll rely entirely on Alex’s GameState class for this information — no direct GUI code here.

---

Functions You’ll Use from Alex’s File

You will use these functions directly from GameStatus_5120.py:

state.get_legal_moves()
state.get_new_state(move)
state.is_terminal()
state.get_scores()
state.is_ai_turn()

These give you everything you need to run your search algorithms.

---

Evaluation Function (AI Scoring)

The AI needs a way to assign a number value to each position so it knows which boards are good or bad.

Rules for your scoring function:
	•	If the AI wins → return a large positive number (e.g., +10,000).
	•	If the human wins → return a large negative number (e.g., -10,000).
	•	If it’s a draw → return 0.
	•	Otherwise, use the difference in triplet counts:

ai_score, opp_score = state.get_scores()
return 100 * (ai_score - opp_score)



This keeps the AI aware of “who’s ahead” during the game.

---

Depth (Difficulty)

The “depth” parameter controls how smart the AI is.

Depth	Description	Typical Use
1–2	Easy	AI only looks one move ahead.
3–4	Medium	Balanced play on 4×4 and 5×5 boards.
5–8	Hard	Perfect play on 3×3 boards.

You’ll make sure this is adjustable so Alex can let players change the difficulty in the GUI.

---

Optimization

To make the AI fast and smart:
	•	Use Alpha-Beta pruning to skip bad moves early.
	•	Implement move ordering (center moves first, then corners).
	•	Add a debug flag so you can print information when needed:

DEBUG = True
if DEBUG:
    print("Depth:", depth, "Best move:", move)



You can also track how many nodes (board states) the AI explores per turn to display in the GUI.

---

Collaboration Details

Teammate	What You Need From Them	What You Give Back
Alex	GameState functions (get_legal_moves(), get_new_state(), etc.)	Your working choose_ai_move() function that plugs into his GUI.
Aparajita	Unit tests for correctness and runtime	Feedback on whether the AI behaves correctly and passes all tests.
Lyssa	Screenshots or explanations of your algorithms	Clear, commented code so she can describe your AI in the report.


---

How You’ll Know You’re Done
	•	The AI plays legal, smart moves.
	•	The game runs smoothly without freezing or crashing.
	•	Minimax, Alpha-Beta, and Negamax all give correct results.
	•	The AI performs well at different depths.
	•	Aparajita’s tests pass without errors.
	•	Alex’s GUI correctly calls your choose_ai_move() every turn.
	•	Lyssa has enough info and visuals for the report.

---

Your Deliverables

File	Description
multiAgents.py	Contains all your AI algorithms and logic.
choose_ai_move()	Function used by GUI to get the AI’s next move.
(Optional) Debug prints or node counters	For transparency and performance testing.


---

Extra Ideas (Optional)
	•	Add a difficulty level system (Easy, Medium, Hard) tied to depth.
	•	Print the AI’s chosen move and score after each turn for clarity.
	•	Add comments describing the purpose of each algorithm step for Lyssa’s report.

---

Quick Summary
	•	You’re building the AI logic that powers the computer opponent.
	•	Your code reads the game state from Alex’s file and decides the next move.
	•	You’ll write Minimax, Alpha-Beta, and Negamax.
	•	The GUI will call your single entry point choose_ai_move() every time it’s the AI’s turn.
	•	Your focus: correctness, performance, and clarity.

---

Would you like me to now write that Team Workflow section (in Markdown) that shows the order everyone works and depends on each other — so you can put it at the top of your Notion workspace? It’ll be a one-page roadmap (who starts first, who depends on who, who finishes last).