#####################################################################
#  This is the destination for your shortest_path code.
#  Take all the cells from your notebook vacuum.ipynb and copy the code
#  into this file.
#
#  Now go to work on your go home agent, in gohomeagent.py
#  Notice that the agent code already imports this function

from agents.searchClientInterface import WorldState
from agents.searchClientInterface import Problem
from agents.searchClientInterface import BFSEvaluator
from agents.searchFramework import aStarSearch
import copy

class ShortestPathWorldState(WorldState):
    
    def __init__(self, start_square, free_squares):
        self._current_square = start_square
        self._free_squares = set(free_squares)
    
    # Convenience function to make these objects print nicely
    def __str__(self):
        return "{" + str(self._square) + "}"
    
    def __eq__(self, other):
        return self._current_square == other._current_square

    def __hash__(self):
        return hash(self._current_square)
    
    #  Create a successor state for every square that is adjacent 
    #  to the current state's current position
    
    def successors(self):
        return [self.make_adjacent_state(adj) for adj in self.adjacencies(self._current_square)] 
    
    #  This is the state where we move from _square to the square
    #  Remember this function has to return a pair (newState, action)
    #  For our path planning, the "action" will be the next square in the path.
    #  For example, if the current square is (2,2) and the adjacency passed in is (1,2)
    #  then this function would return (<state where current square is (1,2)>, (1,2))
    #  That is, in the new state the agent is at square (1,2) and (1,2) is also added
    #  to the action list
    
    def make_adjacent_state(self, adjacency):
        # Check if the adjacency is a valid move
        if adjacency in self._free_squares:
            new_state = ShortestPathWorldState(adjacency, self._free_squares - {adjacency})
            return new_state, adjacency
        else:
            return None
    
    # Return a list of all the squares in the free_squares list that are adjacent
    # to the square passed as parameter.
    # For example if the "current square" is (2,2) then all the adjacent squares
    # are (1,2), (2,1), (2,3), (3,2) -- but you want to return only those squares
    # that are on the free_square_list that was passed in via the constructor

    def adjacencies(self, square):
        adjacent_squares = [(square[0] - 1, square[1]), (square[0] + 1, square[1]),
                            (square[0], square[1] - 1), (square[0], square[1] + 1)]
        return [adj for adj in adjacent_squares if adj in self._free_squares]


#  Now define the problem:  a problem is the initial square, the destination square, 
#  and the list of free squares

class ShortestPathProblem(Problem):
    
    def __init__(self, initial_square, dest_square, free_squares):
        self.initial_square = initial_square
        self.dest_square = dest_square
        self.free_squares = set(free_squares) 

    def initial(self):
        return ShortestPathWorldState(self.initial_square, self.free_squares)

    def isGoal(self, state):
        return state._current_square == self.dest_square


def shortest_path(source_square, dest_square, free_square_list):
    if source_square == dest_square:
        return []

    # Create a ShortestPathProblem instance with the given parameters
    problem = ShortestPathProblem(source_square, dest_square, free_square_list)

    # Perform A* search using BFSEvaluator
    solution = aStarSearch(problem, BFSEvaluator())

    # Extract and return the path from the solution
    path = solution[0] if solution else []  
    return path