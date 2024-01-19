# Working but wrong colors !!!
# from searchClientInterface import Evaluator, DFSEvaluator, WorldState, Problem
# from searchFramework import aStarSearch
# import time

# locations = ['WA', 'OR', 'ID', 'CA', 'NV', 'UT', 'AZ', 'CO', 'NM']
# colors = ["red", "green", "blue", "yellow"]
# adjacencies = [('WA', 'OR'), ('WA', 'ID'), ('OR', 'ID'), ('OR', 'CA'),
#                ('ID', 'CA'), ('CA', 'NV'), ('ID', 'NV'), ('ID', 'UT'),
#                ('CA', 'UT'), ('NV', 'UT'), ('NV', 'AZ'), ('UT', 'AZ'),
#                ('AZ', 'CO'), ('NM', 'AZ')]

# class GCWorldState(WorldState):
#     def __init__(self, assignments):
#         self.assignments = assignments

#     def get_assignments(self):
#         return [(loc, color) for loc, color in self.assignments.items()]

#     def successors(self):
#         unassigned_locations = [loc for loc in locations if self.assignments[loc] is None]
#         current_loc = unassigned_locations[0]

#         successor_states = []
#         for color in colors:
#             if self.is_color_valid(current_loc, color):
#                 new_assignments = self.assignments.copy()
#                 new_assignments[current_loc] = color
#                 successor_states.append((GCWorldState(new_assignments), f"Assign {color} to {current_loc}"))

#         return successor_states

#     def is_color_valid(self, location, color):
#         for adj_loc in [adj for adj in locations if (location, adj) in adjacencies or (adj, location) in adjacencies]:
#             if self.assignments[adj_loc] == color:
#                 return False
#         return True

# class GCProblem(Problem):
#     def __init__(self, locations, colors, adjacencies):
#         self.locations = locations
#         self.colors = colors
#         self.adjacencies = adjacencies

#     def initial(self):
#         return GCWorldState({location: None for location in self.locations})

#     def isGoal(self, state):
#         return all(state.assignments[loc] is not None for loc in self.locations)

# def mapColor(locations, colors, adjacencies):
#     soln, stats = aStarSearch(GCProblem(locations, colors, adjacencies), DFSEvaluator(), verbose=True, limit=50000)
#     return soln

# def solveWesternStates():
#     soln, stats = aStarSearch(GCProblem(locations, colors, adjacencies), DFSEvaluator(), verbose=True, limit=50000)
#     return soln[0].worldState().get_assignments()

# print(mapColor(locations, colors, adjacencies))

###

from searchClientInterface import Evaluator, DFSEvaluator, WorldState, Problem
from searchFramework import aStarSearch
from itertools import cycle

locations = ['WA', 'OR', 'ID', 'CA', 'NV', 'UT', 'AZ', 'CO', 'NM']
colors = ["red", "green", "blue", "yellow"]
adjacencies = [('WA', 'OR'), ('WA', 'ID'), ('OR', 'ID'), ('OR', 'CA'),
               ('ID', 'CA'), ('CA', 'NV'), ('ID', 'NV'), ('ID', 'UT'),
               ('CA', 'UT'), ('NV', 'UT'), ('NV', 'AZ'), ('UT', 'AZ'),
               ('AZ', 'CO'), ('NM', 'AZ')]

class GCWorldState(WorldState):
    def __init__(self, assignments=None):
        self.assignments = assignments or {}

    def get_assignments(self):
        return [(loc, color) for loc, color in self.assignments.items()]

    def successors(self):
        unassigned_locations = [loc for loc in locations if self.assignments.get(loc) is None]

        if not unassigned_locations:
            return []

        current_loc = unassigned_locations[0]
        assigned_colors = set(self.assignments.get(loc) for loc in self.assignments if self.assignments.get(loc) is not None)

        successor_states = []
        for color in colors:
            if self.is_color_valid(current_loc, color):
                new_assignments = self.assignments.copy()
                new_assignments[current_loc] = color
                successor_states.append((GCWorldState(new_assignments), f"Assign {color} to {current_loc}"))

        return successor_states

    def is_color_valid(self, location, color):
        for adj_loc in [adj for adj in locations if (location, adj) in adjacencies or (adj, location) in adjacencies]:
            if self.assignments.get(adj_loc) == color:
                return False
        return True


class GCProblem(Problem):
    def __init__(self, locations, colors, adjacencies):
        self.locations = locations
        self.colors = colors
        self.adjacencies = adjacencies

    def initial(self):
        return GCWorldState({location: None for location in self.locations})

    def isGoal(self, state):
        return all(state.assignments[loc] is not None for loc in self.locations)

def mapColor(locations, colors, adjacencies):
    soln, stats = aStarSearch(GCProblem(locations, colors, adjacencies), DFSEvaluator(), verbose=True, limit=50000)
    return soln

def solveWesternStates():
    soln, stats = aStarSearch(GCProblem(locations, colors, adjacencies), DFSEvaluator(), verbose=True, limit=50000)
    return soln[0].worldState().get_assignments()

print(mapColor(locations, colors, adjacencies))



###: Its working but taking too long to generate colors !!!

# from searchClientInterface import Evaluator, DFSEvaluator, WorldState, Problem
# from searchFramework import aStarSearch
# from itertools import cycle

# locations = ['WA', 'OR', 'ID', 'CA', 'NV', 'UT', 'AZ', 'CO', 'NM']
# colors = ["red", "green", "blue", "yellow"]
# adjacencies = [('WA', 'OR'), ('WA', 'ID'), ('OR', 'ID'), ('OR', 'CA'),
#                ('ID', 'CA'), ('CA', 'NV'), ('ID', 'NV'), ('ID', 'UT'),
#                ('CA', 'UT'), ('NV', 'UT'), ('NV', 'AZ'), ('UT', 'AZ'),
#                ('AZ', 'CO'), ('NM', 'AZ')]

# class GCWorldState(WorldState):
#     def __init__(self, assignments=None):
#         self.assignments = assignments or {}

#     def get_assignments(self):
#         return [(loc, color) for loc, color in self.assignments.items()]

#     def successors(self):
#         unassigned_locations = [loc for loc in locations if self.assignments.get(loc) is None]

#         if not unassigned_locations:
#             return []

#         current_loc = unassigned_locations[0]
#         assigned_colors = set(self.assignments.get(loc) for loc in self.assignments if self.assignments.get(loc) is not None)

#         successor_states = []
#         for color in cycle(colors):
#             if color not in assigned_colors:
#                 new_assignments = self.assignments.copy()
#                 new_assignments[current_loc] = color
#                 action = f"Assign {color} to {current_loc}"
#                 successor_states.append((GCWorldState(new_assignments), action))
#                 break  # Stop after finding one valid color

#         return successor_states

#     def is_color_valid(self, location, color):
#         for adj_loc in [adj for adj in locations if (location, adj) in adjacencies or (adj, location) in adjacencies]:
#             if self.assignments.get(adj_loc) == color:
#                 return False
#         return True

# class GCProblem(Problem):
#     def __init__(self, locations, colors, adjacencies):
#         self.locations = locations
#         self.colors = colors
#         self.adjacencies = adjacencies

#     def initial(self):
#         return GCWorldState()

#     def isGoal(self, state):
#         return all(state.assignments.get(loc) is not None for loc in self.locations)

# def mapColor(locations, colors, adjacencies):
#     soln, stats = aStarSearch(GCProblem(locations, colors, adjacencies), DFSEvaluator(), verbose=True, limit=50000)
#     if soln:
#         assignments = soln[0].worldState().get_assignments()
#         return assignments
#     else:
#         return []
    
# def solveWesternStates():
#     solution = mapColor(locations, colors, adjacencies)
#     if solution:
#         return solution
#     else:
#         return []

# print(mapColor(locations, colors, adjacencies))

