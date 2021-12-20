from typing import Any, Set, Tuple
from grid import Grid
import utils


def locate(grid: Grid, item: Any) -> Set[Tuple[int, int]]:
    '''
    This function takes a 2D grid and an item
    It should return a list of (x, y) coordinates that specify the locations that contain the given item
    To know how to use the Grid class, see the file "grid.py"  
    '''
    # TODO: ADD YOUR CODE HERE
    return {element for element in [(x, y) for y in range(0, grid.height) for x in range(0, grid.width)] if grid.__getitem__(element) == item}
