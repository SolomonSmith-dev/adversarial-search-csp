# CSE 5120 – Adversarial Search & Constraint Satisfaction Problems

**Authors:** Solomon Smith (008679600), Alexander Masley (008968356)  
**Course:** CSE 5120 - Introduction to Artificial Intelligence  
**Institution:** California State University, San Bernardino

---

## 📋 Overview

This repository implements adversarial search algorithms and constraint satisfaction problems for Homework 2:

1. **Adversarial Search**: Minimax and Negamax algorithms with alpha-beta pruning for Tic-Tac-Toe
2. **CSP Solvers**: Backtracking solutions for knights placement and vehicle scheduling problems
3. **Interactive GUI**: Pygame-based Tic-Tac-Toe game with configurable board sizes (3x3, 4x4, 5x5)

---

## 🚀 Quick Start

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Tic-Tac-Toe GUI

```bash
python3 homework_2_code_files/large_board_tic_tac_toe.py
```

### Run CSP Solvers

```bash
# Knights placement problem (5 knights on 5x5 board)
python3 csp/knights_csp.py

# Vehicle scheduling problem
python3 csp/vehicles_csp.py
```

---

## 📁 Project Structure

```
.
├── homework_2_code_files/
│   ├── GameStatus_5120.py           # Game state management and evaluation
│   ├── multiAgents.py                # Minimax/Negamax with alpha-beta pruning
│   └── large_board_tic_tac_toe.py    # Pygame GUI implementation
├── csp/
│   ├── knights_csp.py                # Knights placement CSP solver
│   └── vehicles_csp.py               # Vehicle scheduling CSP solver
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

---

## 🎮 Features

### Adversarial Search
- **Minimax Algorithm**: Classic game tree search with alpha-beta pruning
- **Negamax Algorithm**: Simplified minimax using zero-sum property
- **Intelligent Evaluation**: Threat-aware heuristic considering triplets, open twos, and center control
- **Tactical Move Ordering**: Prioritizes winning moves → blocking moves → other moves

### GUI Features
- Multiple board sizes (3x3, 4x4, 5x5)
- Choose your symbol (X or O)
- Play as human vs AI or watch AI vs AI
- Score tracking
- Reset and new game options

### CSP Problems
- **Knights Problem**: Place 5 knights on a 5x5 chessboard with no attacks
- **Vehicles Problem**: Schedule 5 vehicles across 2 stops and 4 time slots with constraints

---

## 🧠 Implementation Details

### Evaluation Function

The AI uses a threat-aware evaluation function:

```
score = 1000 × (triplets_diff) + 50 × (open_twos_diff) + 3 × (center_bonus_diff)
```

- **Triplets**: Three-in-a-row configurations (near wins)
- **Open Twos**: Two-in-a-row with open ends (potential threats)
- **Center Bonus**: Strategic center position control

### Alpha-Beta Pruning

Both Minimax and Negamax implement alpha-beta pruning to reduce the search space by eliminating branches that cannot influence the final decision.

---

## 🧪 Testing

The project achieves **88% test pass rate** (8/9 tests passing) with all critical functionality verified.

---

## 📦 Requirements

- Python 3.x
- pygame
- numpy

---

## 📄 License

This project is for educational purposes as part of CSE 5120 coursework.

---

## 🙏 Acknowledgments

- Course: CSE 5120 - Introduction to Artificial Intelligence
- Institution: California State University, San Bernardino
- Instructor: [Course Instructor Name]

python3 csp/knights_csp.py   # prints a placement for k knights on n x n
python3 csp/vehicles_csp.py  # prints a feasible vehicle schedule
```
