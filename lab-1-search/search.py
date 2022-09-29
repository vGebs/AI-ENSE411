# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    visited = {}
    stack = util.Stack()

    # We need to keep track of the directions to a given coordinate from the start coordinate
    # If we just log all of our moves in one array, it will be unintelligible
    # There will be 'forks in the road' so we need to keep track of those forks by
    #   giving each node a set of directions that updates upon the last set of directions
    #
    # After we check to see if the coordinate has been visited, we can then check to see if
    #   we landed on the target
    #   Otherwise push all neighbor nodes onto the fringe that encapsulate the newLocation with the directions from the start
    stack.push((problem.getStartState(), []))

    while not stack.isEmpty():
        # explore first child
        coordinate, directions = stack.pop()

        if coordinate not in visited:
            visited[coordinate] = True

            if problem.isGoalState(coordinate):
                return directions
            else:
                for newLocation, direction, cost in problem.getSuccessors(coordinate):
                    newDirections = directions + [direction]
                    stack.push((newLocation, newDirections))

    return directions


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    visited = {}
    queue = util.Queue()

    queue.push((problem.getStartState(), [], 0))

    while not queue.isEmpty():
        coordinate, directions, cost = queue.pop()

        if coordinate not in visited:
            visited[coordinate] = True

            if problem.isGoalState(coordinate):
                return directions
            else:
                for newCoordinate, direction, newCost in problem.getSuccessors(coordinate):
                    newDirections = directions + [direction]
                    updatedCost = cost + newCost
                    queue.push((newCoordinate, newDirections, updatedCost))

    return directions


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    # ok, so we need to first understand UCS
    # after that we need to figure out how to identify the least cost path then return it
    # need to use priority queue

    pQueue = util.PriorityQueue()
    visited = {}

    pQueue.push((problem.getStartState(), [], 0), 0)

    while not pQueue.isEmpty():
        coordinate, directions, cost = pQueue.pop()

        if coordinate not in visited:
            visited[coordinate] = True

            if problem.isGoalState(coordinate):
                return directions
            else:
                for newCoordinate, direction, newCost in problem.getSuccessors(coordinate):
                    newDirections = directions + [direction]
                    updatedCost = cost + newCost
                    pQueue.update((newCoordinate, newDirections,
                                   updatedCost), updatedCost)

    return directions


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    # A* score = (cost of path) + heuristic

    # print(problem.getSuccessors(problem.getStartState()))
    # print(heuristic(problem.getStartState(), problem))

    pQueue = util.PriorityQueue()
    visited = {}

    pQueue.push((problem.getStartState(), [], 0),
                heuristic(problem.getStartState(), problem))

    while not pQueue.isEmpty():
        coordinate, directions, cost = pQueue.pop()

        if coordinate not in visited:
            visited[coordinate] = True

            if problem.isGoalState(coordinate):
                return directions
            else:
                for newCoordinate, direction, newCost in problem.getSuccessors(coordinate):
                    newDirections = directions + [direction]
                    updatedCost = cost + newCost
                    priority = updatedCost + heuristic(newCoordinate, problem)
                    pQueue.update((newCoordinate, newDirections,
                                   updatedCost), priority)

    return directions


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
