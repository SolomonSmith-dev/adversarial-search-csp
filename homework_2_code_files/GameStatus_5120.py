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
        YOUR CODE HERE TO CHECK IF ANY CELL IS EMPTY WITH THE VALUE 0. IF THERE IS NO EMPTY
        THEN YOU SHOULD ALSO RETURN THE WINNER OF THE GAME BY CHECKING THE SCORES FOR EACH PLAYER 
        """
        rows = len(self.board_state)
        cols = len(self.board_state[0])
        k = self.win_length

        # Check horizontal triplets
        for r in range(rows):
            for c in range(cols - 2):
                s = (
                    self.board_state[r][c]
                    + self.board_state[r][c + 1]
                    + self.board_state[r][c + 2]
                )
                if s == k:
                    self.winner = "AI"
                    return True
                elif s == -k:
                    self.winner = "Human"
                    return True

        # Check vertical triplets
        for c in range(cols):
            for r in range(rows - 2):
                s = (
                    self.board_state[r][c]
                    + self.board_state[r + 1][c]
                    + self.board_state[r + 2][c]
                )
                if s == k:
                    self.winner = "AI"
                    return True
                elif s == -k:
                    self.winner = "Human"
                    return True

        # Check diagonal (top-left to bottom-right)
        for r in range(rows - 2):
            for c in range(cols - 2):
                s = (
                    self.board_state[r][c]
                    + self.board_state[r + 1][c + 1]
                    + self.board_state[r + 2][c + 2]
                )
                if s == k:
                    self.winner = "AI"
                    return True
                elif s == -k:
                    self.winner = "Human"
                    return True

        # Check diagonal (bottom-left to top-right)
        for r in range(2, rows):
            for c in range(cols - 2):
                s = (
                    self.board_state[r][c]
                    + self.board_state[r - 1][c + 1]
                    + self.board_state[r - 2][c + 2]
                )
                if s == k:
                    self.winner = "AI"
                    return True
                elif s == -k:
                    self.winner = "Human"
                    return True

        # If any empty cell exists, game is not terminal yet on larger boards
        # The game ends when the board is full.
        for r in range(rows):
            for c in range(cols):
                if self.board_state[r][c] == 0:
                    return False

        # No empty cells, the game is over.
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
        rows = len(self.board_state)
        cols = len(self.board_state[0])
        scores = 0

        if self.human_symbol == "X":
            human_player, ai_player = -1, 1
        else:
            human_player, ai_player = 1, -1

        # Helper to evaluate a "window" of 3 cells
        def evaluate_window(window):
            score = 0
            human_pieces = window.count(human_player)
            ai_pieces = window.count(ai_player)
            empty_cells = window.count(0)

            if human_pieces == 3:
                score += 100  # Human wins
            elif ai_pieces == 3:
                score -= 100  # AI wins
            elif human_pieces == 2 and empty_cells == 1:
                score += 10  # Human has a threat
            elif ai_pieces == 2 and empty_cells == 1:
                score -= 10  # AI has a threat
            elif human_pieces == 1 and empty_cells == 2:
                score += 1 # Human has a potential
            elif ai_pieces == 1 and empty_cells == 2:
                score -= 1 # AI has a potential
            return score

        # Horizontal check
        for r in range(rows):
            for c in range(cols - 2):
                window = [self.board_state[r][c], self.board_state[r][c+1], self.board_state[r][c+2]]
                scores += evaluate_window(window)

        # Vertical check
        for c in range(cols):
            for r in range(rows - 2):
                window = [self.board_state[r][c], self.board_state[r+1][c], self.board_state[r+2][c]]
                scores += evaluate_window(window)

        # Diagonal checks (top-left to bottom-right)
        for r in range(rows - 2):
            for c in range(cols - 2):
                window = [self.board_state[r][c], self.board_state[r+1][c+1], self.board_state[r+2][c+2]]
                scores += evaluate_window(window)

        # Diagonal checks (bottom-left to top-right)
        for r in range(2, rows):
            for c in range(cols - 2):
                window = [self.board_state[r][c], self.board_state[r-1][c+1], self.board_state[r-2][c+2]]
                scores += evaluate_window(window)
        
        return scores

    def get_negamax_scores(self, terminal):
        """
        YOUR CODE HERE TO CALCULATE NEGAMAX SCORES. THIS FUNCTION SHOULD EXACTLY BE THE SAME OF GET_SCORES UNLESS
        YOU SET THE SCORE FOR NEGAMX TO A VALUE THAT IS NOT AN INCREMENT OF 1 (E.G., YOU CAN DO SCORES = SCORES + 100 
                                                                               FOR HUMAN PLAYER INSTEAD OF 
                                                                               SCORES = SCORES + 1) For now, reuse get_scores to keep behavior identical.
        """
    
        return self.get_scores(terminal)

    def get_moves(self):
        moves = []
        """
        YOUR CODE HERE TO ADD ALL THE NON EMPTY CELLS TO MOVES VARIABLES AND RETURN IT TO BE USE BY YOUR
        MINIMAX OR NEGAMAX FUNCTIONS
        """
        rows = len(self.board_state)
        cols = len(self.board_state[0])

        for r in range(rows):
            for c in range(cols):
                if self.board_state[r][c] == 0:
                    moves.append((r, c))
        return moves

    def get_new_state(self, move):
        # Make a shallow copy of each row to avoid mutating the original board.
        new_board_state = [row.copy() for row in self.board_state]
        x, y = move[0], move[1]
        new_board_state[x][y] = 1 if self.turn_O else -1
        return GameStatus(new_board_state, not self.turn_O, self.human_symbol)
