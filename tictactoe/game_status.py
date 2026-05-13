# -*- coding: utf-8 -*-



class GameStatus:
    def __init__(self, board_state, turn_O, human_symbol="X"):
        self.board_state = board_state
        self.turn_O = turn_O
        self.human_symbol = human_symbol  # Track which symbol human is using
        self.oldScores = 0
        self.winner = ""
        self.win_length = 3

    def _dims(self):
        # Get board dimensions
        R = len(self.board_state)
        C = len(self.board_state[0])
        return R, C

    def _human_val(self):
        """Return the board encoding for the human player (+1 for O, -1 for X)."""
        sym = getattr(self, "human_symbol", "X")
        return 1 if str(sym).upper() == "O" else -1

    def _sequences(self, L=None):
        # Yield all sequences of length L (row, col, diag)
        if L is None:
            L = self.win_length
        R, C = self._dims()
        B = self.board_state
        for r in range(R):
            for c in range(C - L + 1):
                yield [B[r][c + k] for k in range(L)], ("row", r, c)
        for c in range(C):
            for r in range(R - L + 1):
                yield [B[r + k][c] for k in range(L)], ("col", r, c)
        for r in range(R - L + 1):
            for c in range(C - L + 1):
                yield [B[r + k][c + k] for k in range(L)], ("diag_dr", r, c)
        for r in range(R - L + 1):
            for c in range(L - 1, C):
                yield [B[r + k][c - k] for k in range(L)], ("diag_dl", r, c)

    # ---------- Heuristic helpers + relative eval ----------
    def _count_triplets_for(self, val):
        """Completed 3-in-a-rows for a given player value."""
        L = self.win_length
        cnt = 0
        for seq, _ in self._sequences(L):
            if all(v == val for v in seq):
                cnt += 1
        return cnt

    def _count_open_twos_for(self, val):
        """
        Number of 2-in-a-row with the third empty within a length-3 window.
        Only used for 3-in-a-row games.
        """
        L = self.win_length
        if L != 3:
            return 0
        cnt = 0
        for seq, _ in self._sequences(3):
            if seq.count(val) == 2 and seq.count(0) == 1:
                cnt += 1
        return cnt

    def _center_bonus_for(self, val):
        """Small positional nudge for classic 3x3 center control."""
        R, C = self._dims()
        if (R % 2 == 1) and (C % 2 == 1):
            return 1 if self.board_state[R // 2][C // 2] == val else 0
        return 0

    def evaluate_relative(self):
        """
        Heuristic from the perspective of the side to move.
        Positive => good for the player to move; negative => good for opponent.
        """
        me = 1 if self.turn_O else -1     # board encoding: 1 = 'O', -1 = 'X'
        them = -me

        my_trips   = self._count_triplets_for(me)
        thm_trips  = self._count_triplets_for(them)
        my_twos    = self._count_open_twos_for(me)
        thm_twos   = self._count_open_twos_for(them)
        my_center  = self._center_bonus_for(me)
        thm_center = self._center_bonus_for(them)

        base    = 1000 * (my_trips - thm_trips)   # force wins/blocks
        threats =   50 * (my_twos  - thm_twos)    # immediate threats
        pos     =    3 * (my_center - thm_center) # small positional

        return base + threats + pos
    # -------------------------------------------------------------------

    def is_terminal(self):
        human_val = self._human_val()
        # Check for a win mid-game
        for seq, _ in self._sequences():
            if seq[0] != 0 and all(v == seq[0] for v in seq[1:]):
                self.winner = "Human" if seq[0] == human_val else "AI"
                return True
        # Check if board is full
        for row in self.board_state:
            if 0 in row:
                return False
        # Board is full with no winner: draw
        self.winner = "DRAW"
        return True

    def get_scores(self, terminal):
        # Count triplets for human and AI
        L = self.win_length
        human_val = self._human_val()
        ai_val = -human_val
        human = 0
        ai = 0
        for seq, _meta in self._sequences(L):
            if all(v == human_val for v in seq):
                human += 1
            elif all(v == ai_val for v in seq):
                ai += 1
        score = human - ai
        if terminal and score != 0:
            return 1000 if score > 0 else -1000
        return score

    def get_negamax_scores(self, terminal):
        """
        Return a value from the mover's perspective for negamax.
        For terminal (full board) reuse the final ±1000/0 outcome.
        """
        if terminal:
            return self.get_scores(terminal=True)
        return self.evaluate_relative()

    def get_moves(self):
        # Return all empty cells
        moves = []
        for r, row in enumerate(self.board_state):
            for c, v in enumerate(row):
                if v == 0:
                    moves.append((r, c))
        return moves

    def opponent_winning_moves_next(self):
        """
        Identify blocking moves: positions where if we DON'T play,
        the opponent can win on their next turn.
        
        Returns:
            set: Moves we should prioritize to prevent opponent wins
        """
        opponent = -1 if self.turn_O else 1
        winning = set()
        for move in self.get_moves():
            test_state = self.get_new_state(move)
            # After our move, it's opponent's turn
            # Check if opponent can win on their next move
            for opp_move in test_state.get_moves():
                final_state = test_state.get_new_state(opp_move)
                if final_state._count_triplets_for(opponent) > test_state._count_triplets_for(opponent):
                    winning.add(move)
                    break
        return winning

    def winning_moves_for_current_player(self):
        """
        Find all moves that immediately create a triplet (win) for current player.
        
        Returns:
            list: Moves that win the game immediately
        """
        current = 1 if self.turn_O else -1
        winning = []
        for move in self.get_moves():
            test_state = self.get_new_state(move)
            if test_state._count_triplets_for(current) > self._count_triplets_for(current):
                winning.append(move)
        return winning

    def get_new_state(self, move):
        # Return new GameStatus after move
        if hasattr(self.board_state[0], 'copy'):
            new_board_state = [row.copy() for row in self.board_state]
        else:
            new_board_state = [list(row) for row in self.board_state]
        x, y = move[0], move[1]
        new_board_state[x][y] = 1 if self.turn_O else -1
        return GameStatus(new_board_state, not self.turn_O, self.human_symbol)
