from GameStatus_5120 import GameStatus
import random


def minimax(game_state: GameStatus, depth: int, maximizing_player: bool, alpha=float('-inf'), beta=float('inf')):
    terminal = game_state.is_terminal()
    if (depth == 0) or (terminal):
        newScores = game_state.get_scores(terminal)
        return newScores, None

    """
    YOUR CODE HERE TO FIRST CHECK WHICH PLAYER HAS CALLED THIS FUNCTION (MAXIMIZING OR MINIMIZING PLAYER)
    YOU SHOULD THEN IMPLEMENT MINIMAX WITH ALPHA-BETA PRUNING AND RETURN THE FOLLOWING TWO ITEMS
    1. VALUE
    2. BEST_MOVE
    
    THE LINE TO RETURN THESE TWO IS COMMENTED BELOW WHICH YOU CAN USE
    """
    if maximizing_player:
        maxEval = float('-inf')
        best_moves = []  # Store all moves with the best evaluation

        for move in game_state.get_moves():
            new_state = game_state.get_new_state(move)
            evaluation = minimax(new_state, depth - 1, False, alpha, beta)[0]
            if evaluation > maxEval:
                maxEval = evaluation
                best_moves = [move]  # New best, reset list
            elif evaluation == maxEval:
                best_moves.append(move)  # Tie with current best, add to list
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        # Randomly choose among equally good moves
        best_move = random.choice(best_moves) if best_moves else None
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_moves = []  # Store all moves with the best evaluation

        for move in game_state.get_moves():
            new_state = game_state.get_new_state(move)
            evaluation = minimax(new_state, depth - 1, True, alpha, beta)[0]
            if evaluation < minEval:
                minEval = evaluation
                best_moves = [move]  # New best, reset list
            elif evaluation == minEval:
                best_moves.append(move)  # Tie with current best, add to list
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        # Randomly choose among equally good moves
        best_move = random.choice(best_moves) if best_moves else None
        return minEval, best_move

def negamax(game_status: GameStatus, depth: int, turn_multiplier: int, alpha=float('-inf'), beta=float('inf')):
    terminal = game_status.is_terminal()
    if (depth == 0) or (terminal):
        # Negamax requires score from the current player's perspective.
        # get_scores() is from human's perspective.
        # turn_multiplier is 1 for human, -1 for AI.
        # So, score * turn_multiplier gives the score for the current player.
        scores = game_status.get_negamax_scores(terminal) * turn_multiplier 
        return scores, None

    """
    YOUR CODE HERE TO CALL NEGAMAX FUNCTION. REMEMBER THE RETURN OF THE NEGAMAX SHOULD BE THE OPPOSITE OF THE CALLING
    PLAYER WHICH CAN BE DONE USING -NEGAMAX(). THE REST OF YOUR CODE SHOULD BE THE SAME AS MINIMAX FUNCTION.
    YOU ALSO DO NOT NEED TO TRACK WHICH PLAYER HAS CALLED THE FUNCTION AND SHOULD NOT CHECK IF THE CURRENT MOVE
    IS FOR MINIMAX PLAYER OR NEGAMAX PLAYER
    RETURN THE FOLLOWING TWO ITEMS
    1. VALUE
    2. BEST_MOVE

    THE LINE TO RETURN THESE TWO IS COMMENTED BELOW WHICH YOU CAN USE

    """
    maxEval = float('-inf')
    best_moves = []  # Store all moves with the best evaluation

    for move in game_status.get_moves():
        new_state = game_status.get_new_state(move)

        evaluation = -negamax(new_state, depth - 1, -turn_multiplier, -beta, -alpha)[0]
        if evaluation > maxEval:
            maxEval = evaluation
            best_moves = [move]  # New best, reset list
        elif evaluation == maxEval:
            best_moves.append(move)  # Tie with current best, add to list
        alpha = max(alpha, evaluation)
        if beta <= alpha:
            break
    
    # Randomly choose among equally good moves
    best_move = random.choice(best_moves) if best_moves else None
    return maxEval, best_move