# adversarial-search-csp

[![tests](https://github.com/SolomonSmith-dev/adversarial-search-csp/actions/workflows/test.yml/badge.svg)](https://github.com/SolomonSmith-dev/adversarial-search-csp/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/downloads/)

Adversarial search and constraint satisfaction problem solvers in Python.

Four deliverables in one repo:

1. **Minimax and Negamax** with alpha-beta pruning, plugged into a Tic-Tac-Toe engine that supports 3x3, 4x4, and 5x5 boards.
2. **Pygame GUI** for human vs AI or AI vs AI play, with score tracking and variable board size.
3. **A game-agnostic negamax core** (`games/`) that drives both Connect Four and Tic-Tac-Toe from a single search implementation.
4. **CSP backtracking solvers**, including a generic framework with MRV ordering and forward checking, applied to three combinatorial problems: N-Queens, placing knights on a chessboard with no attacks, and scheduling 5 vehicles across 2 stops and 4 time slots.

Author: Solomon Smith.

## Quickstart

```bash
git clone https://github.com/SolomonSmith-dev/adversarial-search-csp.git
cd adversarial-search-csp
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Tic-Tac-Toe GUI (3x3 / 4x4 / 5x5 selectable in-app)
python3 tictactoe/large_board_tic_tac_toe.py

# Tic-Tac-Toe in the terminal (no display required)
python3 tictactoe/play_cli.py                  # human (X) vs AI on 3x3
python3 tictactoe/play_cli.py --mode ai_vs_ai  # watch two perfect AIs draw
python3 tictactoe/play_cli.py --size 4 --algorithm minimax --depth 3

# Connect Four in the terminal (same negamax core as Tic-Tac-Toe)
python3 games/play_connect_four.py                 # human (X) vs AI
python3 games/play_connect_four.py --mode ai_vs_ai --depth 5

# CSP solvers (prints a valid assignment to stdout)
python3 csp/knights_csp.py            # default 5 knights on 5x5
python3 csp/knights_csp.py -n 8 -k 8  # configurable board size and count
python3 csp/vehicles_csp.py
python3 csp/vehicles_csp.py --graph   # emit the constraint graph as Graphviz DOT
python3 csp/nqueens_csp.py -n 8       # N-Queens on the generic CSP framework
```

Requires Python 3.x and pygame 2.6.1 (pinned in `requirements.txt`).

## Algorithms

### Minimax with alpha-beta pruning

Standard game-tree search to a configurable depth. MAX (human) and MIN (AI) alternate. Alpha-beta pruning eliminates branches that cannot affect the final decision. At terminal states the algorithm returns the actual triplet count; at non-terminal leaves it returns a heuristic evaluation. Code: `tictactoe/multiAgents.py`.

### Negamax with alpha-beta pruning

Same search, simpler scaffolding. Exploits the zero-sum property: a single recursive function handles both players by scoring every node from the side-to-move's perspective and negating the recursive result. No duplicated MAX/MIN branches.

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

### Game-agnostic search core

`games/search.py` holds a negamax + alpha-beta search that knows nothing about any specific game. It operates on any object satisfying a small `GameState` protocol (`is_terminal`, `score`, `legal_moves`, `make_move`, `order_moves`), where `score` is always from the side-to-move's perspective.

The same search drives two unrelated games:

- **Connect Four** (`games/connect_four.py`): a native `GameState` with gravity, four-in-a-row detection (horizontal, vertical, both diagonals), and a window-based heuristic. Center-out column ordering keeps alpha-beta lean (a depth-6 search from the empty 7x6 board explores under 2000 nodes). Board size and the win length are configurable.
- **Tic-Tac-Toe** (`games/tictactoe_adapter.py`): a thin adapter wrapping the existing `GameStatus` engine, so the identical negamax plays it with no duplicated game logic.

That reuse is asserted directly in the tests: one `negamax` picks correct moves for both games.

```bash
python3 games/play_connect_four.py --mode ai_vs_ai --depth 5
```

## CSP solvers

The knights and vehicle solvers use plain backtracking with unary-constraint propagation at domain construction time. The N-Queens solver runs on a small **generic CSP framework** (`csp/backtracking.py`) with two classic optimizations.

### Generic framework (`csp/backtracking.py`)

A reusable `CSP` core: declare variables and domains, attach `Constraint` objects, and call `backtracking_search`. It supports:

- **MRV (minimum-remaining-values)** variable ordering: always branch on the most constrained variable first, so dead ends surface early.
- **Forward checking**: after each assignment, prune now-impossible values from neighboring domains and abandon the branch the moment any domain empties.

Both are toggleable, and the search returns a `SearchStats` record (nodes explored, backtracks, prunings) so the payoff is measurable. On 8-Queens, the node count drops from **876** (naive backtracking) to **75** (MRV + forward checking):

```
$ python3 csp/nqueens_csp.py -n 8
Solution for 8 queens:
Q . . . . . . .
...
[nodes=75 backtracks=67 prunings=291]
```

### N-Queens (`csp/nqueens_csp.py`)

Place `N` queens on an `N x N` board with no two attacking. One variable per column (value = the queen's row), with a single pairwise no-same-row/diagonal constraint. Solvable for all `n` except 2 and 3. Flags `--no-mrv` and `--no-forward-checking` turn the optimizations off to compare search sizes.

### Knights placement (`csp/knights_csp.py`)

Place `k` knights on an `n x n` board so none attack any other. The script prints one valid placement for the configured `n` and `k`.

### Vehicle scheduling (`csp/vehicles_csp.py`)

Schedule 5 vehicles (A through E) across 2 stops (CGI, JB_Hall) and 4 time slots, with unary constraints (e.g. B must arrive at slot 1) and pairwise constraints (no two vehicles at the same stop in the same slot taking the same action).

## Project structure

```
.
├── tictactoe/
│   ├── game_status.py              # game state and terminal-state evaluation
│   ├── multiAgents.py              # Minimax + Negamax with alpha-beta pruning
│   ├── play_cli.py                 # headless terminal driver (no display needed)
│   └── large_board_tic_tac_toe.py  # pygame GUI
├── games/
│   ├── search.py                   # game-agnostic negamax + alpha-beta
│   ├── connect_four.py             # Connect Four as a GameState
│   ├── tictactoe_adapter.py        # GameStatus adapted to the same search
│   └── play_connect_four.py        # headless Connect Four CLI
├── csp/
│   ├── backtracking.py             # generic CSP core (MRV + forward checking)
│   ├── nqueens_csp.py              # N-Queens on the generic framework
│   ├── knights_csp.py              # knights placement CSP solver
│   └── vehicles_csp.py             # vehicle scheduling CSP solver
├── tests/                          # pytest suite
├── pyproject.toml                  # project metadata and pytest config
├── requirements.txt
└── README.md
```

## Testing

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

53 tests across the `GameStatus` class, the minimax and negamax algorithms, the headless CLI (including a perfect-self-play-always-draws regression), Connect Four and the game-agnostic search core (including tests that one search plays both games), the generic CSP framework (including a test that forward checking shrinks the search), and all three CSP solvers. CI runs the suite on every push and pull request.

## License

MIT. See [LICENSE](LICENSE).
