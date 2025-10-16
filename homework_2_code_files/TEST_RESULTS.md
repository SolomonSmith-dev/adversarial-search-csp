# Algorithm Test Results

## Test Suite Summary (Updated October 16, 2025)

### Overall Results

9/9 tests passed (100%)

### ✅ Passing Tests

1. Blocking Move
2. Winning Move
3. Fork Opportunity
4. Center Preference
5. Human as O
6. Terminal State Detection
7. Draw Detection
8. 4x4 Board Support
9. Alpha-Beta Pruning Consistency

## Key Changes That Improved Results

- Increased terminal win/loss scoring magnitude in `get_scores()` to ±1000 so immediate wins dominate heuristic evaluation.
- In minimax/negamax, added short-circuiting to immediately choose moves that create terminal wins for the player to move.
- Added deterministic tie-breaking: prefer terminal moves, then center, then corners, then others. This stabilized the "Center Preference" test and improved move quality.

## Notes on Behavior

- Tie-breaking keeps gameplay varied when multiple moves are equally optimal, but prioritizes strong strategic choices.
- The algorithms work for configurable board sizes (3x3, 4x4, 5x5) with win_length=3.

## Running the Tests

```bash
cd homework_2_code_files
python test_algorithms.py
```

## Conclusion

The minimax and negamax implementations are fully functional and pass all automated tests. The AI reliably blocks threats, takes wins, and makes strong opening choices.
