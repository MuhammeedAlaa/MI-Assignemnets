from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use
import math

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the tree value and the best action


def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1, depth: int = 0) -> Tuple[float, A]:
    #get the terminal condation and the utility
    terminal = game.is_terminal(state)
    #check if this state is a termianl state to return the utility
    if terminal[0]: return (terminal[1][0], None)
    #check the depth to return the heuristic for the max depth from the current state
    if depth == max_depth: return (heuristic(game, state, 0), None)
    # get all action with successors
    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    #if it is maximizer
    if game.get_turn(state) == 0:
        #define the value and the action to maximize
        intermediate_a = None
        intermediate_v = -math.inf
        #for all the successors states we get the max value it can get
        for a, s in actions_states:
            v = minimax(game, s, heuristic, max_depth, depth + 1)[0]
            if v > intermediate_v: 
                intermediate_v, intermediate_a = v, a 
        return intermediate_v, intermediate_a
    #if it is minimizer
    else:
        intermediate_v = math.inf
        intermediate_a = None
        #for all the successors states we get the min value it can get
        for a, s in actions_states:
            v = minimax(game, s, heuristic, max_depth, depth + 1)[0]
            if v <= intermediate_v: 
                intermediate_v, intermediate_a = v, a 
        return intermediate_v, intermediate_a


# Apply Alpha Beta pruning and return the tree value and the best action
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1, depth: int = 0, alpha: int = -math.inf, beta: int = math.inf) -> Tuple[float, A]:
    #get the terminal condation and the utility
    terminal = game.is_terminal(state)
    #check if this state is a termianl state to return the utility
    if terminal[0]: return (terminal[1][0], None)
    #check the depth to return the heuristic for the max depth from the current state
    if depth == max_depth: return (heuristic(game, state, 0), None)
    # get all action with successors
    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    #if it is maximizer
    if game.get_turn(state) == 0:
        #define the value and the action to maximize
        intermediate_a = None
        intermediate_v = -math.inf
        #for all the successors states we get the max value it can get
        for a, s in actions_states:
            v = alphabeta(game, s, heuristic, max_depth, depth + 1, alpha, beta)[0]
            if v > intermediate_v: 
                intermediate_v, intermediate_a = v, a 
            #check the brun condtion
            if intermediate_v >= beta: return intermediate_v, intermediate_a
            alpha = max(alpha, intermediate_v)
    #if it is minimizer
    else:
        #define the value and the action to minmize
        intermediate_v = math.inf
        intermediate_a = None
        #for all the successors states we get the min value it can get
        for a, s in actions_states:
            v = alphabeta(game, s, heuristic, max_depth, depth + 1, alpha, beta)[0]
            if v <= intermediate_v: 
                intermediate_v, intermediate_a = v, a
            #check the brun condtion
            if intermediate_v <= alpha: return intermediate_v, intermediate_a
            beta = min(beta, intermediate_v)
    return intermediate_v, intermediate_a

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1, depth: int = 0, alpha: int = -math.inf, beta: int = math.inf) -> Tuple[float, A]:
    #get the terminal condation and the utility
    terminal = game.is_terminal(state)
    #check if this state is a termianl state to return the utility
    if terminal[0]: return (terminal[1][0], None)
    #check the depth to return the heuristic for the max depth from the current state
    if depth == max_depth: return (heuristic(game, state, 0), None)
    # get all action with successors
    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

    her_order = [(-heuristic(game, state, 0), index) for index, (_ , state) in enumerate(actions_states)]
    #sort based on the agent
    if game.get_turn(state) == 0:
        her_order.sort()
    else:
        her_order.sort(reverse=True)
    actions_states = [actions_states[ind] for _, ind in her_order]
    
    #if it is maximizer
    if game.get_turn(state) == 0:
        #define the value and the action to maximize
        intermediate_a = None
        intermediate_v = -math.inf
        #for all the successors states we get the max value it can get
        for a, s in actions_states:
            v = alphabeta_with_move_ordering(game, s, heuristic, max_depth, depth + 1, alpha, beta)[0]
            if v > intermediate_v: 
                intermediate_v, intermediate_a = v, a 
            #check the brun condtion
            if intermediate_v >= beta: return intermediate_v, intermediate_a
            alpha = max(alpha, intermediate_v)
    #if it is minimizer      
    else:
        #define the value and the action to minimize
        intermediate_v = math.inf
        intermediate_a = None
        #for all the successors states we get the min value it can get
        for a, s in actions_states:
            v = alphabeta_with_move_ordering(game, s, heuristic, max_depth, depth + 1, alpha, beta)[0]
            if v <= intermediate_v: 
                intermediate_v, intermediate_a = v, a
            if intermediate_v <= alpha: return intermediate_v, intermediate_a
            #check the brun condtion
            beta = min(beta, intermediate_v)
    return intermediate_v, intermediate_a

# Apply Expectimax search and return the tree value and the best action
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1, depth: int = 0) -> Tuple[float, A]:
    #get the terminal condation and the utility
    terminal = game.is_terminal(state)
    #check if this state is a termianl state to return the utility
    if terminal[0]: return (terminal[1][0], None)
    #check the depth to return the heuristic for the max depth from the current state
    if depth == max_depth: return (heuristic(game, state, 0), None)
    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    if game.get_turn(state) == 0:
        #define the value and the action to maximize
        intermediate_a = None
        intermediate_v = -math.inf
        #for all the successors states we get the max value it can get
        for a, s in actions_states:
            v = expectimax(game, s, heuristic, max_depth, depth + 1)[0]
            if v > intermediate_v: 
                intermediate_v, intermediate_a = v, a 
        return intermediate_v, intermediate_a
    #if it is expicti 
    else:
        #calculate the avarge
        avg = 0
        for a, s in actions_states:
            avg += expectimax(game, s, heuristic, max_depth, depth + 1)[0]
        return avg / len(actions_states), None
