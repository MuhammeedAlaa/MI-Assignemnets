from typing import List
from dungeon import DungeonGame, DungeonState
from mathutils import Direction, Point

# Return the path length or a very large number if the path is None
def path_length(path) -> int:
    return 0xffffffff if path is None else len(path)-1

# Return the path between two points in the dungeom
# The result is cached inside the game object
def compute_path(game: DungeonGame, p1: Point, p2: Point) -> List[Point]:
    cache = game.cache()
    if p1 not in cache:
        from collections import deque
        path_map = {p1: [p1]}
        queue = deque([p1])
        while queue:
            parent = queue.popleft()
            path = path_map[parent]
            for direction in Direction:
                child = parent + direction.to_vector()
                if child in path_map or child not in game.layout.walkable:
                    continue
                path_map[child] = path + [child]
                queue.append(child)
        cache[p1] = path_map
    return cache[p1].get(p2, None)

# Finds the shortest path from a point to a path in the dungeon
def path_to_path(game: DungeonGame, p1: Point, path: List[Point]):
    if path is None: return None
    paths = [compute_path(game, p1, p2) for p2 in path]
    _, _, shortest = min((path_length(path), index, path) for index, path in enumerate(paths))
    return shortest

# Checks if monsters can reach the player while traversing the shortest path to a goal point
# Returns the number of monster that endanger the player and the length of the player's path
def path_safety(game: DungeonGame, state: DungeonState, goal: Point):
    path = compute_path(game, state.player.position, goal)
    length = path_length(path)
    # For each alive monster, find the shortest path from the the monster to the player's path
    monster_paths = [path_to_path(game, monster.position, path) for monster in state.monsters if monster.alive]
    # Find how long the monster will take to reach the player's path
    monster_path_lengths = [path_length(monster_path) for monster_path in monster_paths]
    # Find how it will take the player to get past the monster encounter position
    monster_encounter_distance = [path.index(monster_path[-1]) for monster_path in monster_paths]
    # Count dangerous monsters (the ones that can reach the player path before the player can outpace them)
    danger = sum(encounter >= distance for encounter, distance in zip(monster_encounter_distance, monster_path_lengths))
    return danger, length

# Returns a heuristic value for the dungeon game state
# Argument:
# - game: the game that is being played
# - state: the state to evaluate
# - agent: the agent for which we are evaluating the state. For example, if the value is high for the player, it should be low for the monster
# Returns the heuristic value of the state for the given agent 
def dungeon_heuristic(game: DungeonGame, state: DungeonState, agent: int) -> float:
    area = state.layout.width * state.layout.height

    value = state.score()
    INFINITY = int(1e8)
    if state.player.inventory.keys != 0 and state.player.position == state.layout.exit:
        # If the player won, return a very high value for the player (very low for the monsters)
        value += INFINITY
        return value if agent == 0 else -value
    if not state.player.alive:
        # If the player lost, return a very lowe value for the player (very high for the monsters)
        value = -INFINITY
        return value if agent == 0 else -value
    
    # Incentivize the player to collect a key
    value += area * min(1, state.player.inventory.keys)
    alive_monsters = [monster for monster in state.monsters if monster.alive]
    # Incentivize the player to kill monsters (voilence is always the anwser)
    value -= len(alive_monsters)
    # Incentivize the player to collect as many daggers as needed to kill the remaining monsters
    value += 10 * min(len(alive_monsters), state.player.inventory.daggers)

    # find the distance to the nearest monster
    if alive_monsters:
        nearest_monster = min(path_length(compute_path(game, state.player.position, monster.position)) for monster in alive_monsters)
    else:
        nearest_monster = area
    

    # Now we check the situation of the player and give them points accordingly
    if state.player.inventory.keys == 0:
        # Situation: Has no keys, must find key
        danger, distance = min(path_safety(game, state, key) for key in state.keys)
        if danger <= state.player.inventory.daggers:
            value += 2 * area # No danger bonus
            # Seek key
            value -= distance # distance to key penalty
        elif len(state.daggers) == 0:
            # There are no daggers to collect so seek key anyway
            value -= distance # distance penalty
            if nearest_monster < 2: value -= area * area # penalize being too near to a monster
        else:
            # Situation: seek dagger
            danger, distance = min(path_safety(game, state, dagger) for dagger in state.daggers)
            if danger <= 0: value += area  # No danger bonus
            elif nearest_monster < 2: value -= area * area # penalize being too near to a monster
            value -= distance # distance to dagger penalty
    else:
        # Situation: Has key, must reach exit
        value += 4 * area # Bonus for having the key
        danger, distance = path_safety(game, state, state.layout.exit)
        if danger <= state.player.inventory.daggers:
            value += 2 * area # No danger bonus
            # Seek exit
            value -= distance # distance to exit penalty
        elif len(state.daggers) == 0:
            # Seek exit anyway
            value -= distance # distance to exit penalty
            if nearest_monster < 2: value -= area * area # penalize being too near to a monster
        else:
            # Situation: seek dagger
            danger, distance = min(path_safety(game, state, dagger) for dagger in state.daggers)
            if danger <= 0: value += area  # No danger bonus
            elif nearest_monster < 2: value -= area * area # penalize being too near to a monster
            value -= distance # distance to dagger penalty

    # if the agent is a monster, return the negative of the value
    return value if agent == 0 else -value