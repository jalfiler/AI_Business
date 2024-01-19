#1
## First define your world state
##  You should represent your actions as follows:
##     ("fill", "3cap" ) and ("fill", "7cap")
##     ("empty" "3cap") and ("empty", "7cap")
##     ("pour", "3cap", <amount>) and ("pour", "7cap", <amount)  -- where for example
##        ("pour", "3cap")   means "Pour from the 3cap jug to the 7cap jug"
##              The rules above determine how much water is actually poured

from searchClientInterface import WorldState
import copy

class JugWorldState(WorldState):
    def __init__(self, capacities, levels):
        self.capacities = capacities
        self.levels = levels

    def successors(self):
        successors = []
        for i in range(len(self.capacities)):
            for j in range(len(self.capacities)):
                if i != j:
                    # Pour water from jug i to jug j
                    amount_poured = min(self.levels[i], self.capacities[j] - self.levels[j])
                    if amount_poured > 0:  # Check if pouring makes a difference
                        new_levels = self.levels.copy()
                        new_levels[i] -= amount_poured
                        new_levels[j] += amount_poured
                        successors.append((JugWorldState(self.capacities, new_levels), f"Pour Jug{i+1} to Jug{j+1}"))
        
        # Fill or empty each jug individually
        for i in range(len(self.capacities)):
            # Fill jug i
            fill_levels = self.levels.copy()
            fill_levels[i] = self.capacities[i]
            if fill_levels != self.levels:  # Check if filling makes a difference
                successors.append((JugWorldState(self.capacities, fill_levels), f"Fill Jug{i+1}"))

            # Empty jug i
            empty_levels = self.levels.copy()
            empty_levels[i] = 0
            if empty_levels != self.levels:  # Check if emptying makes a difference
                successors.append((JugWorldState(self.capacities, empty_levels), f"Empty Jug{i+1}"))

        return successors


#2
from searchClientInterface import Problem

class JugProblem(Problem):
    def __init__(self, capacities, initials, goals):
        self.capacities = capacities
        self.initials = initials
        self.goals = goals

    def initial(self):
        return JugWorldState(self.capacities, self.initials)

    def isGoal(self, state):
        return state.levels == self.goals


#3
from searchClientInterface import BFSEvaluator, DFSEvaluator
from searchFramework import aStarSearch

# Define the problem
initial = [0, 0]
goal = [0, 5]
problem = JugProblem([3, 7], initial, goal)

# Test A* search with BFSEvaluator
bfs_evaluator = BFSEvaluator()
bfs_result, bfs_stats = aStarSearch(problem, bfs_evaluator)
print("BFS Result:", bfs_result)
print("BFS Stats:", bfs_stats)

# Test A* search with DFSEvaluator
dfs_evaluator = DFSEvaluator()
dfs_result, dfs_stats = aStarSearch(problem, dfs_evaluator, limit=1000)
print("DFS Result:", dfs_result)
print("DFS Stats:", dfs_stats)
