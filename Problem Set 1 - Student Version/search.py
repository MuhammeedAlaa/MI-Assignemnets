from problem import HeuristicFunction, Problem, S, A, Solution
from queue import PriorityQueue

# TODO: Import any modules or write any helper functions you want to use


def CostSearch(problem: Problem[S, A], initial_state: S, type: int, heuristic: HeuristicFunction):
    frontier = PriorityQueue()  # create pqueue
    count = 1  # this counter to handle if 2 states have same cost take the first in
    # frontier queue have the cost , count , initial state, path
    frontier.put((0, count, initial_state, []))
    explored = {}  # explored set
    while not frontier.empty():
        # pop the min cost and first in the queue
        (oldCost, _, node, path) = frontier.get()
        if node not in explored:  # if it is not explored
            explored[node] = 0  # add it to explored set
            if problem.is_goal(node):  # if it is a goal retun the path to it
                return path
            # for each reachable action from the current state
            for action in problem.get_actions(node):
                child = problem.get_successor(node, action)  # we get the child
                if type == 0:  # this if else statements just for modularity 0 uniform cost, 1 A*, 2 Greedy
                    cost = oldCost + problem.get_cost(node, child)
                elif type == 1:
                    cost = oldCost - heuristic(problem, node) + problem.get_cost(
                        node, child) + heuristic(problem, child)
                else:
                    cost = heuristic(problem, child)
                count += 1  # increase the counter
                # put the child in frontier to explore it after
                frontier.put((cost, count, child, path + [action]))
    return None


# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution


def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # declar the frontier list and explored set and paths to hold the solution
    frontier = [(initial_state, [])]
    explored = {}
    while frontier:  # if the frontier is empty meens that no path for the goal
        # get last node from the queue to explore it
        (node, path) = frontier.pop(0)
        if node not in explored:  # check of it is already in explored set so we don't explore it again
            explored[node] = 0
            if problem.is_goal(node):  # if the current child is a goal
                # next code till the return just for back traking if we found a goal
                return path
            # for all possible actions from the current node
            for action in problem.get_actions(node):
                # get the successor from the current node with a given action
                child = problem.get_successor(node, action)
                # if the successor not in explored or frontier we safe to check cause it will be check for the first time
                if child not in explored:
                    # adding the child to the queue
                    frontier.append((child, path + [action]))
    return None


def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # declar the frontier list and explored set and paths to hold the solution
    frontier = [(initial_state, [])]
    explored = {}
    while frontier:  # if the frontier is empty meens that no path for the goal
        # get last node from the queue to explore it
        (node, path) = frontier.pop()
        if node not in explored:  # check of it is already in explored set so we don't explore it again
            explored[node] = 0
            if problem.is_goal(node):  # if the current child is a goal
                # next code till the return just for back traking if we found a goal
                return path
            # for all possible actions from the current node
            for action in problem.get_actions(node):
                # get the successor from the current node with a given action
                child = problem.get_successor(node, action)
                # if the successor not in explored or frontier we safe to check cause it will be check for the first time
                if child not in explored:
                    # adding the child to the queue
                    frontier.append((child, path + [action]))
    return None


def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    return CostSearch(problem, initial_state, 0, None)


def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:

    return CostSearch(problem, initial_state, 1, heuristic)


def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    return CostSearch(problem, initial_state, 2, heuristic)
