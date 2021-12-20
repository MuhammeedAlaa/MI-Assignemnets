import networkx as nx
from itertools import combinations
import numpy as np
from dungeon import DungeonProblem, DungeonState
from mathutils import Direction, euclidean_distance, manhattan_distance
from problem import Problem
# This heuristic returns the distance between the player and the exit as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal


def weak_heuristic(problem: DungeonProblem, state: DungeonState):
    return euclidean_distance(state.player, problem.layout.exit)


# TODO: Import any modules and write any functions you want to use

def bfs(start, end, walkable):  # bfs function but betwwen points
    frontier = [(start, [])]  # put the first point in frontier list
    explored = {}
    while frontier:  # until the frontier not empty
        (node, path) = frontier.pop(0)  # put left most element
        if node not in explored:  # if this not not explored before
            explored[node] = 0  # explore it
            if node == end:  # if we reach the goal return the path
                return len(path)
            # for every action
            for action in [Direction.UP, Direction.DOWN, Direction.RIGHT, Direction.LEFT]:
                # get the result between current action and result
                child = node + action.to_vector()
                if child not in walkable:  # if we can't do it we will be in same state
                    child = node
                # if next state (child state) not in frontier add it
                if child not in explored:
                    frontier.append((child, path + [action]))
    return None


def build_adj_matrix(problem, initial_state, remaining_coins):
    # check if we are in the initial_state we build the adj_matrix for coins and save it in cache
    if initial_state != remaining_coins:
        coins_indices = {c: i for i, c in enumerate(
            remaining_coins)}  # get the indices of coins
        # build a zero matrix with the remaining_coins length
        coins_count = len(remaining_coins)
        adj_matrix = np.zeros((coins_count, coins_count))
        # for every combinations of 2 coins we get the distance between them and but it in the adj_matrix if not in cache
        for coin1, coin2 in combinations(remaining_coins, 2):
            i, j = coins_indices[coin1], coins_indices[coin2]
            if(coin1, coin2) not in problem.cache():
                adj_matrix[i, j] = adj_matrix[j, i] = bfs(
                    coin1, coin2, problem.layout.walkable)
            else:
                adj_matrix[i, j] = problem.cache()[(coin1, coin2)]
        problem.cache()['adj_matrix'] = adj_matrix
    else:  # if we are not in initail state we get the adj_matrix from cache
        adj_matrix = problem.cache()['adj_matrix']
        coins_indices = {c: i for i, c in enumerate(remaining_coins)}
        # if a coin is taken we update the adj_matrix and save it
        for coin in set(remaining_coins).difference(set(initial_state.remaining_coins)):
            index = coins_indices[coin]
            adj_matrix[index, :] = adj_matrix[:, index] = 0
        problem.cache()['adj_matrix'] = adj_matrix

    return adj_matrix


def get_distance_from_mst(adj_matrix):
    # we build mst for the coins to get the minimum distance that span all the coins
    G = nx.from_numpy_matrix(adj_matrix)
    mst = nx.minimum_spanning_tree(G)
    return sum(e[2]['weight'] for e in mst.edges(data=True))


def get_distance_from_min_coin(problem, state):
    # we get the distance between the current state and the coins to get the minimum coin distance
    path_to_coin = []
    for coin in state.remaining_coins:  # for each coin if the distance not in cahse we do bfs on it
        if (state.player, coin) not in problem.cache():
            player_coin_distance = bfs(
                state.player, coin, problem.layout.walkable)
            path_to_coin.append(player_coin_distance)
            problem.cache()[(state.player, coin)] = problem.cache()[
                (coin, state.player)] = player_coin_distance
        else:
            path_to_coin.append(problem.cache()[(state.player, coin)])
    return min(path_to_coin) if len(path_to_coin) else 0


def strong_heuristic(problem: DungeonProblem, state: DungeonState) -> float:
    # TODO: ADD YOUR CODE HERE
    # IMPORTANT: DO NOT USE "problem.is_goal" HERE.
    # Calling it here will mess up the tracking of the explored nodes count
    # which is considered the number of is_goal calls during the search
    # NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function

    initial_state = problem.get_initial_state()
    remaining_coins = state.remaining_coins
    adj_matrix = build_adj_matrix(problem, initial_state, remaining_coins)
    distance_mst = get_distance_from_mst(adj_matrix)
    distance_min_coin = get_distance_from_min_coin(problem, state)
    return distance_mst + distance_min_coin
