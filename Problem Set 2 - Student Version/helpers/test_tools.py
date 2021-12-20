from typing import List, Tuple
from tree import TreeGame, TreeNode, tree_heuristic
from dungeon import DungeonGame, Direction
from dungeon_heuristic import dungeon_heuristic
from .utils import Result, fetch_recorded_calls, fetch_tracked_call_count, load_function
from .pruned_tree import pruned_tree_string

# Checks if two floating point numbers are almost equal
def approx_eq(output, expected):
    return abs(output - expected)/(abs(output) + abs(expected)) < 1e-8

# Runs a testcase on a tree game 
def run_search_for_tree(
    function_path: str, 
    game: TreeGame) -> Tuple[List[str], List[str]]:

    fetch_recorded_calls(TreeGame.is_terminal) # Clear the recorded calls

    search_fn = load_function(function_path) # Load the search function
    
    initial_state = game.get_initial_state() # Get the initial state
    # Search without a depth limit
    value, action = search_fn(game, initial_state, tree_heuristic, -1)
    
    # get a list of nodes that have been explored by the search function
    explored = [call["args"][1] for call in fetch_recorded_calls(TreeGame.is_terminal)]
    
    return value, action, [node.name for node in explored]

# Compare a testcase result with the expected output on a tree game
def compare_search_results_for_tree(
    output: Tuple[float, str, List[str]],
    possible_outputs: List[Tuple[float, str, List[str]]],
    tree_path: str) -> Result:

    # Check if the result is one of the expected values
    # If yes, return a success result
    value, action, explored = output
    for expected_value, expected_action, expected_explored in possible_outputs:
        if approx_eq(value, expected_value) and action == expected_action and explored == expected_explored:
            return Result(True, 1, "")
    
    tree = TreeNode.from_file(tree_path) # Read the tree from a file to display in the failure message
    
    # Since it is not a success, create and return a failure result with a failure message
    nl = '\n'
    list_to_str = lambda l: repr(l) + "\n" + pruned_tree_string(tree, l) #
    out_to_str = lambda o: f'- Value: {o[0]} / Action: {o[1]} {nl}- Explored {len(o[2])} Nodes: {list_to_str(o[2])}'
    expected = '\nor\n'.join(out_to_str(expected) for expected in possible_outputs)
    message = f"Tree:{nl}{tree}{nl}Expected:{nl}{expected}{nl}Got:{nl}{out_to_str(output)}"
    
    return Result(False, 0, message)

# Runs a testcase on a dungeon game
def run_search_for_dungeon(
    function_path: str, 
    game: DungeonGame,
    max_search_depth: int) -> Tuple[float, Direction, int]:

    fetch_tracked_call_count(DungeonGame.is_terminal) # Clear the recorded calls
    
    search_fn = load_function(function_path) # Load the search function
    
    initial_state = game.get_initial_state() # Get the initial state
    # Search with the specified depth limit
    value, action = search_fn(game, initial_state, dungeon_heuristic, max_search_depth)
    
    # get the count of nodes that have been explored by the search function
    explored = fetch_tracked_call_count(DungeonGame.is_terminal)

    return value, action, explored

# Compare a testcase result with the expected output on a dungeon game
def compare_search_results_for_dungeon(
    output: Tuple[float, Direction, int],
    possible_outputs: List[Tuple[float, Direction, int]],
    level_path: str) -> Result:
    
    # Check if the result is one of the expected values
    # If yes, return a success result
    value, action, explored = output
    for expected_value, expected_action, expected_explored in possible_outputs:
        if approx_eq(value, expected_value) and action == expected_action and explored == expected_explored:
            return Result(True, 1, f"Explored {explored} nodes")
    
    # Since it is not a success, create and return a failure result with a failure message
    nl = '\n'
    expected = '\nor\n'.join(f'- Value: {value} / Action: {str(action)}{nl}- Explored {explored} nodes' for value, action, explored in possible_outputs)
    level = open(level_path, 'r').read()
    message = f"Level:{nl}{level}{nl}Expected:{nl}{expected}{nl}Got:{nl}- Value: {output[0]} / Action: {str(output[1])}{nl}- Explored {output[2]} nodes"
    return Result(False, 0, message)