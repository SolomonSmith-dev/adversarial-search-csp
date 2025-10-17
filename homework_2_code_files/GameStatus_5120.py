# -*- coding: utf-8 -*-


class GameStatus:

    def __init__(self, board_state, turn_O, human_symbol="X"):
        self.board_state = board_state
        self.turn_O = turn_O
        self.human_symbol = human_symbol  # Track which symbol human is using
        self.oldScores = 0
        self.winner = ""
        # Length of sequence required for a win/triplet counting
        self.win_length = 3

    def _dims(self):
        R = len(self.board_state)
        C = len(self.board_state[0])
        return R, C

    def _sequences(self, L=None):
        """Yield (sequence_list, (type, r, c)) for each contiguous sequence of length L.

        type is one of 'row', 'col', 'diag_dr', 'diag_dl' and (r,c) is the starting
        coordinate for that sequence (top-left for rows/cols/diag_dr, top-right for diag_dl).
        """
        if L is None:
            L = self.win_length
        R, C = self._dims()
        B = self.board_state

        # rows
        for r in range(R):
            for c in range(C - L + 1):
                yield [B[r][c + k] for k in range(L)], ("row", r, c)

        # cols
        for c in range(C):
            for r in range(R - L + 1):
                yield [B[r + k][c] for k in range(L)], ("col", r, c)

        # diag down-right
        for r in range(R - L + 1):
            for c in range(C - L + 1):
                yield [B[r + k][c + k] for k in range(L)], ("diag_dr", r, c)

        # diag down-left
        for r in range(R - L + 1):
            for c in range(L - 1, C):
                yield [B[r + k][c - k] for k in range(L)], ("diag_dl", r, c)

    def is_terminal(self):
        """
        For 3x3, the game ends immediately when any 3-in-a-row is present.
        For larger boards, the game ends only when the board is full; the winner
        is then decided by counting triplets.
        """
        R, C = self._dims()
        L = self.win_length

        # Quick check for immediate winner on 3x3
        if R == 3 and C == 3:
            for seq, _meta in self._sequences(L):
                if seq[0] != 0 and all(v == seq[0] for v in seq):
                    winner_val = seq[0]
                    human_val = 1 if str(self.human_symbol).upper() == 'O' else -1
                    self.winner = "Human" if winner_val == human_val else "AI"
                    return True
            # no immediate winner; if any empty cell exists the game is not terminal
            for row in self.board_state:
                if 0 in row:
                    return False
            # board full: determine winner by triplet counts
            score = self.get_scores(terminal=True)
            if score > 0:
                self.winner = "Human"
            elif score < 0:
                self.winner = "AI"
            else:
                self.winner = "DRAW"
            return True

        # larger boards: end only when full
        for row in self.board_state:
            if 0 in row:
                return False
        score = self.get_scores(terminal=True)
        if score > 0:
            self.winner = "Human"
        elif score < 0:
            self.winner = "AI"
        else:
            self.winner = "DRAW"
        return True

    def get_scores(self, terminal):
        """
        Count the number of winning-length sequences for human and AI.
        Returns human_count - ai_count (positive -> human ahead, negative -> AI ahead).
        If terminal and non-zero, return a dominant value (±1000) to guide search.
        """
        L = self.win_length
        sym = getattr(self, "human_symbol", "X")
        human_val = 1 if str(sym).upper() == "O" else -1
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
        # Keep same behavior as get_scores for now
        return self.get_scores(terminal)

    def get_moves(self):
        """Returns list of all empty cells (row, col)."""
        moves = []
        for r, row in enumerate(self.board_state):
            for c, v in enumerate(row):
                if v == 0:
                    moves.append((r, c))
        return moves

    def get_new_state(self, move):
        # Make a shallow copy of each row to avoid mutating the original board.
        # Handle both numpy arrays and lists
        if hasattr(self.board_state[0], 'copy'):
            new_board_state = [row.copy() for row in self.board_state]
        else:
            # For lists, convert to list of lists
            new_board_state = [list(row) for row in self.board_state]
        x, y = move[0], move[1]
        new_board_state[x][y] = 1 if self.turn_O else -1
        return GameStatus(new_board_state, not self.turn_O, self.human_symbol)
