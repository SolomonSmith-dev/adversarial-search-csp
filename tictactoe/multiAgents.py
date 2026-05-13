from game_status import GameStatus
import random


def ordered_moves(state):
    """
    Order moves tactically: winning moves first, then blocking moves, then others.
    This improves alpha-beta pruning efficiency.
    """
    winning = set(state.winning_moves_for_current_player())
    opp_wins = set(state.opponent_winning_moves_next())
    moves = state.get_moves()
    wins = [m for m in moves if m in winning]
    blocks = [m for m in moves if m in opp_wins and m not in winning]
    others = [m for m in moves if m not in winning and m not in opp_wins]
    return wins + blocks + others


def choose_tiebreak(state, candidates):
    """
    Break ties between equally-good moves by preferring center, then corners, then random.
    This adds strategic preference without affecting correctness.
    """
    if not candidates:
        return None
    R, C = len(state.board_state), len(state.board_state[0])
    center = (R // 2, C // 2)
    corners = {(0, 0), (0, C - 1), (R - 1, 0), (R - 1, C - 1)}
    
    if center in candidates:
        return center
    corner_choices = [m for m in candidates if m in corners]
    return random.choice(corner_choices) if corner_choices else random.choice(candidates)


def minimax(game_state, depth, maximizing_player, alpha=float('-inf'), beta=float('inf')):
    # Minimax with alpha-beta pruning
    terminal = game_state.is_terminal()
    if depth == 0 or terminal:
        if terminal:
            return game_state.get_scores(True), None  # final ±1000/0
        # non-terminal leaf: threat-aware, from MAX perspective
        eval_score = game_state.evaluate_relative()
        if not maximizing_player:
            eval_score = -eval_score
        return eval_score, None
    if maximizing_player:
        maxEval = float('-inf')
        best_moves = []
        
        for move in ordered_moves(game_state):
            new_state = game_state.get_new_state(move)
            if new_state.is_terminal():
                evaluation = new_state.get_scores(True)
            else:
                evaluation = minimax(new_state, depth - 1, False, alpha, beta)[0]
            if evaluation > maxEval:
                maxEval = evaluation
                best_moves = [move]
            elif evaluation == maxEval:
                best_moves.append(move)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        
        best_move = choose_tiebreak(game_state, best_moves)
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_moves = []
        
        for move in ordered_moves(game_state):
            new_state = game_state.get_new_state(move)
            if new_state.is_terminal():
                evaluation = new_state.get_scores(True)
                if evaluation < 0:
                    return evaluation, move
            else:
                evaluation = minimax(new_state, depth - 1, True, alpha, beta)[0]
            if evaluation < minEval:
                minEval = evaluation
                best_moves = [move]
            elif evaluation == minEval:
                best_moves.append(move)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        
        best_move = choose_tiebreak(game_state, best_moves)
        return minEval, best_move

def negamax(game_status, depth, alpha=float('-inf'), beta=float('inf')):
    # Negamax with alpha-beta pruning
    terminal = game_status.is_terminal()
    if depth == 0 or terminal:
        # Use threat-aware, player-relative evaluation
        scores = game_status.get_negamax_scores(terminal)
        return scores, None
    
    maxEval = float('-inf')
    best_moves = []
    
    for move in ordered_moves(game_status):
        new_state = game_status.get_new_state(move)
        if new_state.is_terminal():
            evaluation = new_state.get_negamax_scores(True)  # no * turn_multiplier
            if evaluation > maxEval:
                maxEval = evaluation
                best_moves = [move]
            if evaluation > 0:
                return maxEval, move
        else:
            evaluation = -negamax(new_state, depth - 1, -beta, -alpha)[0]
        if evaluation > maxEval:
            maxEval = evaluation
            best_moves = [move]
        elif evaluation == maxEval:
            best_moves.append(move)
        alpha = max(alpha, evaluation)
        if beta <= alpha:
            break
    
    best_move = choose_tiebreak(game_status, best_moves)
    return maxEval, best_move