from venv.agents.searchClientInterface import WorldState
from venv.agents.searchClientInterface import Problem
from venv.agents.searchClientInterface import BFSEvaluator
from venv.agents.searchFramework import aStarSearch
import copy

# Return the shortest path from source_pos to dest_pos that goes only through
# positions in free_pos_list, and such that every position in the path is 
# adjacent to the position of the next element of the path.   For example, 
# in a 3-3 grid where there is a wall at (2,2) a path from (3,2) to (1,2) might
# look like this:
#   shortest_path((3,2), (1,2), [(1,1), (1,2), (1,3), (2,1), (2,3), (3,1), (3,2), (3,3)])
#       ->  [(3,3), (2,3), (1,3), (1,2)] 
# Notice that the first (begin) position does not appear in the output path, but the 
# last (end) position does

def shortest_path(source_pos, dest_pos, free_pos_list):
    path = aStarSearch(ShortestPathProblem(source_pos, dest_pos, free_pos_list), BFSEvaluator())[0]
    return path
    
class ShortestPathWorldState(WorldState):
    def __init__(self, position, free_squares):
        self._free_squares = free_squares
        self._position = position
    
    # Return all the positions in free squares that are adjacent to my position
    def adjacencies(self):
        # Your code here
    
    # Is this position adjacent to me?
    def adjacent(self, p):
       # Your code here
       
    # Convenience function to make these objects print nicely
    def __str__(self):
        return "{" + str(self._position) + "}"
    
    #  These two methods are REQUIRED to make cycle checking work
    #  Notice they depend on the object's internal state, so they must
    #  be customized to each new kind of WorldState
    
    def __eq__(self, other):
        if isinstance(other, ShortestPathWorldState):
            return self._position == other._position
        else:
            return False

    def __hash__(self):
        return hash(str(self._position))
    
    # Successors -- all positions in free_squares that are adjacent to self._position
    #  Note that the "action" associated with a successor is the successor position itself.
    #  That is, the transition from position   (1,1) to a successor position (1,2) is 
    #      STATE(1,1)  -- ACTION(1,2) -->  SUCCESSOR_STATE(1,2)
    
    def successors(self):
        return [self.make_adjacent_state(adj) for adj in self.adjacencies(self._position)] 
    
    # Return a pair (newstate, adjacency)  for this position
    def make_adjacent_state(self, adjacency):
        # Your code here
    
class ShortestPathProblem(Problem):
    def __init__(self, source_position, dest_position, free_positions):
        self._source_position = source_position
        self._dest_position = dest_position
        self._free_positions = free_positions

    def initial(self):
        return ShortestPathWorldState(self._source_position, self._free_positions)
    
    def isGoal(self, state):
        return state._position == self._dest_position
