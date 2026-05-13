# adversarial-search-csp

[![tests](https://github.com/SolomonSmith-dev/adversarial-search-csp/actions/workflows/test.yml/badge.svg)](https://github.com/SolomonSmith-dev/adversarial-search-csp/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)

Adversarial search and constraint satisfaction problem solvers built for CSE 5120 (Introduction to AI) at California State University, San Bernardino.

Three deliverables in one repo:

1. **Minimax and Negamax** with alpha-beta pruning, plugged into a Tic-Tac-Toe engine that supports 3x3, 4x4, and 5x5 boards.
2. **Pygame GUI** for human vs AI or AI vs AI play, with score tracking and variable board size.
3. **CSP backtracking solvers** for two combinatorial problems: placing knights on a chessboard with no attacks, and scheduling 5 vehicles across 2 stops and 4 time slots.

Authors: Solomon Smith and Alexander Masley.

## Quickstart

```bash
git clone https://github.com/SolomonSmith-dev/adversarial-search-csp.git
cd adversarial-search-csp
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Tic-Tac-Toe GUI (3x3 / 4x4 / 5x5 selectable in-app)
python3 tictactoe/large_board_tic_tac_toe.py

# CSP solvers (prints a valid assignment to stdout)
python3 csp/knights_csp.py
python3 csp/vehicles_csp.py
```

Requires Python 3.x and pygame 2.6.1 (pinned in `requirements.txt`).

## Algorithms

### Minimax with alpha-beta pruning

Standard game-tree search to a configurable depth. MAX (human) and MIN (AI) alternate. Alpha-beta pruning eliminates branches that cannot affect the final decision. At terminal states the algorithm returns the actual triplet count; at non-terminal leaves it returns a heuristic evaluation. Code: `tictactoe/multiAgents.py`.

### Negamax with alpha-beta pruning

Same search, simpler scaffolding. Exploits the zero-sum property so a single recursive function handles both players via a `turn_multiplier`. No duplicated MAX/MIN branches.

### Evaluation function

The heuristic is threat-aware. For each non-terminal leaf:

```
score = 1000 * triplets_diff + 50 * open_twos_diff + 3 * center_bonus_diff
```

- `triplets_diff` weights near-wins (three-in-a-row patterns).
- `open_twos_diff` weights two-in-a-row patterns with at least one open end.
- `center_bonus_diff` rewards center control on larger boards where it dominates branching.

### Move ordering

Before search, candidate moves are ordered: winning moves first, then blocking moves, then everything else. This makes alpha-beta prune harder on average, which matters at depth on 4x4 and 5x5 boards.

## CSP solvers

Both use plain backtracking with unary-constraint propagation at domain construction time.

### Knights placement (`csp/knights_csp.py`)

Place `k` knights on an `n x n` board so none attack any other. The script prints one valid placement for the assigned configuration.

### Vehicle scheduling (`csp/vehicles_csp.py`)

Schedule 5 vehicles (A through E) across 2 stops (CGI, JB_Hall) and 4 time slots, with unary constraints (e.g. B must arrive at slot 1) and pairwise constraints (no two vehicles at the same stop in the same slot taking the same action).

## Project structure

```
.
├── tictactoe/
│   ├── GameStatus_5120.py          # game state and terminal-state evaluation
│   ├── multiAgents.py              # Minimax + Negamax with alpha-beta pruning
│   └── large_board_tic_tac_toe.py  # pygame GUI
├── csp/
│   ├── knights_csp.py              # knights placement CSP solver
│   └── vehicles_csp.py             # vehicle scheduling CSP solver
├── requirements.txt
└── README.md
```

## Testing

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

21 tests across the `GameStatus` class, the minimax and negamax algorithms, and both CSP solvers. CI runs the suite on every push and pull request.

## License

MIT for the original code in this repo. Course materials (problem statements, board-game framework scaffolding) remain CSUSB property and are included here only for reproducibility.

## Course

CSE 5120, Introduction to Artificial Intelligence. California State University, San Bernardino.
