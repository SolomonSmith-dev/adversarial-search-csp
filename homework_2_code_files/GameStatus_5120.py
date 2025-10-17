# -*- coding: utf-8 -*-


class GameStatus:

    def __init__(self, board_state, turn_O, human_symbol="X"):
        self.board_state = board_state
        self.turn_O = turn_O
        self.human_symbol = human_symbol  # Track which symbol human is using
        self.oldScores = 0
        self.winner = ""
        self.win_length = 3

    def is_terminal(self):
        """
        Terminal only when the board is full.
        For 4×4 and 5×5 the winner is decided by total triplets.
        """
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
                  

    # get_scores function takes the game state (self) and a boolean terminal as input
    def get_scores(self, terminal):
        """
        YOUR CODE HERE TO CALCULATE THE SCORES. MAKE SURE YOU ADD THE SCORE FOR EACH PLAYER BY CHECKING 
        EACH TRIPLET IN THE BOARD IN EACH DIRECTION (HORIZONAL, VERTICAL, AND ANY DIAGONAL DIRECTION)
        
        YOU SHOULD THEN RETURN THE CALCULATED SCORE WHICH CAN BE POSITIVE (HUMAN PLAYER WINS),
        NEGATIVE (AI PLAYER WINS), OR 0 (DRAW)
        """
        B = self.board_state
        R, C = len(B), len(B[0])
        L = getattr(self, "win_length", 3)

        # Human symbol default is X if not set by GUI
        sym = getattr(self, "human_symbol", "X")
        human_val = 1 if str(sym).upper() == "O" else -1
        ai_val = -human_val

        def count_line(seq):
            h = a = 0
            for i in range(len(seq) - L + 1):
                w = seq[i:i+L]
                if all(v == human_val for v in w):
                    h += 1
                elif all(v == ai_val for v in w):
                    a += 1
            return h, a

        human = ai = 0

        # rows
        for r in range(R):
            h, a = count_line(B[r])
            human += h; ai += a

        # cols
        for c in range(C):
            col = [B[r][c] for r in range(R)]
            h, a = count_line(col)
            human += h; ai += a

        # diag down-right
        for r in range(R - L + 1):
            for c in range(C - L + 1):
                diag = [B[r+k][c+k] for k in range(L)]
                h, a = count_line(diag)
                human += h; ai += a

        # diag down-left
        for r in range(R - L + 1):
            for c in range(L - 1, C):
                diag = [B[r+k][c-k] for k in range(L)]
                h, a = count_line(diag)
                human += h; ai += a

        score = human - ai

        # When terminal, make any nonzero result dominant to guide search
        if terminal and score != 0:
            return 1000 if score > 0 else -1000
        return score
    

    def get_negamax_scores(self, terminal):
        """
        YOUR CODE HERE TO CALCULATE NEGAMAX SCORES. THIS FUNCTION SHOULD EXACTLY BE THE SAME OF GET_SCORES UNLESS
        YOU SET THE SCORE FOR NEGAMX TO A VALUE THAT IS NOT AN INCREMENT OF 1 (E.G., YOU CAN DO SCORES = SCORES + 100 
                                                                               FOR HUMAN PLAYER INSTEAD OF 
                                                                               SCORES = SCORES + 1) For now, reuse get_scores to keep behavior identical.
        """
    
        return self.get_scores(terminal)

    def get_moves(self):
        """
        Returns list of all empty cells (value 0) as (row, col) tuples.
        Used by minimax/negamax to find valid moves.
        """
        moves = []
        for r, row in enumerate(self.board_state):
            for c, v in enumerate(row):
                if v == 0:
                    moves.append((r, c))
        return moves

    def get_new_state(self, move):
        # Make a shallow copy of each row to avoid mutating the original board.
        new_board_state = [row.copy() for row in self.board_state]
        x, y = move[0], move[1]
        new_board_state[x][y] = 1 if self.turn_O else -1
        return GameStatus(new_board_state, not self.turn_O, self.human_symbol)
