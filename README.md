# Tic-Tac-Toe Minimax/Negamax Project

This repository contains an implementation of Minimax and Negamax algorithms for a Tic-Tac-Toe variant, with automated tests and a Pygame GUI.

Quick start

1. Run the tests (from the project root):

```bash
cd homework_2_code_files
python3 test_algorithms.py
```

2. Play the game (GUI):

```bash
cd homework_2_code_files
python3 large_board_tic_tac_toe.py
```

Notes
 
- The `homework_2_code_files` folder contains the main working code and tests.
- Tests currently pass 9/9.

## CSE 5120 – Multiagent Search and CSP

## Authors

Solomon Smith - 008679600
Alexander Masley - 008968356

## Overview

This repo contains our implementation of Homework 2 for CSE 5120.  
We built adversarial Tic-Tac-Toe with **Minimax**, **Negamax**, and **Alpha-Beta Pruning**, plus solutions for two **CSP problems**.

## Files

- `multiAgents.py` – search algorithms
- `large_board_tic_tac_toe.py` – Pygame GUI and main loop
- `GameStatus_5120.py` – game state and scoring
- `csp/knights_csp.py` – knights problem
- `csp/vehicles_csp.py` – vehicles scheduling problem

## CSP Demos

Run the included simple CSP solvers/demos:

```bash
python3 csp/knights_csp.py   # prints a placement for k knights on n x n
python3 csp/vehicles_csp.py  # prints a feasible vehicle schedule
```
