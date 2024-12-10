from Model import QueenBee, Grasshopper, Spider, Beetle, SoldierAnt 
from Controller import get_all_valid_moves_for_color 
from state import GameState


def evaluate_game_state(GameState):
    # Implement your heuristic evaluation logic here
    score = 0
    # Add your evaluation logic
    return score



# Minmax no pruning
def minimax(game_state, depth, maximizing_player):
    if depth == 0 or game_state.is_game_over():
        return evaluate_game_state(game_state)

    if maximizing_player:
        max_eval = float('-inf')
        for move in game_state.get_all_valid_moves_for_color():
            game_state.make_move(move)
            eval = minimax(game_state, depth - 1, False)
            game_state.undo_move(move)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in game_state.get_all_valid_moves():
            game_state.make_move(move)
            eval = minimax(game_state, depth - 1, True)
            game_state.undo_move(move)
            min_eval = min(min_eval, eval)
        return min_eval

# Minmax with alpha-beta pruning
def minimax(game_state, depth, alpha, beta, maximizing_player):
    if depth == 0 or game_state.is_game_over():
        return evaluate_game_state(game_state)

    if maximizing_player:
        max_eval = float('-inf')
        for move in game_state.get_all_valid_moves_for_color():
            game_state.make_move(move)
            eval = minimax(game_state, depth - 1, alpha, beta, False)
            game_state.undo_move(move)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in game_state.get_all_valid_moves():
            game_state.make_move(move)
            eval = minimax(game_state, depth - 1, alpha, beta, True)
            game_state.undo_move(move)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval