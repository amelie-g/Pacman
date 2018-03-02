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
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    "*** YOUR CODE HERE ***"
    # set start state
    root = problem.getStartState()

    # create list for visited states
    visitedNodes = set()

    # create stack for states
    stack = util.Stack()

    # add start state to stack
    stack.push((root, []))

    # initialize current state and empty list for actions
    cur_state = None
    game_list = []

    # loop through states while it is not the goal state and the stack is not empty 
    while not stack.isEmpty() and not problem.isGoalState(cur_state):

        # pop state from stack and add it to list of visited states
        cur_state, game_list = stack.pop()
        visitedNodes.add(cur_state)

        # get the successors of popped state
        children = problem.getSuccessors(cur_state)

        # for each successor, get coordinates and direction
        for child in children:
            coor = child[0]
            if not coor in visitedNodes:
                d = child[1]

                # add each child to the stack
                stack.push((coor, game_list + [d]))

    # return list of actions
    return game_list


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # set start state
    root = problem.getStartState()

    # create queue for states
    queue = util.Queue()

    visited_states = []
    # add start state to queue
    queue.push((root, []))

    # initialize current state and empty list for actions
    cur_state = None
    game_list = []

    # loop through list while it isn't empty and while it's not the goal state
    while not queue.isEmpty() and not problem.isGoalState(cur_state):

        # pop state and add it to list of visited states
        cur_state, game_list = queue.pop()

        # get successors of popped state
        children = problem.getSuccessors(cur_state)

        # for each successor, get coordinates and directions
        for child in children:
            coor = child[0]

            d = child[1]
            if coor not in visited_states:
                # add successors to list of visited states
                visited_states.append(coor)

                # add each child to the queue
                queue.push((coor, game_list + [d]))
    # return list of actions
    return game_list


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # set start state
    root = problem.getStartState()

    # create list of visited states
    visitedNodes = []

    # create priority queue for states
    priorityQ = util.PriorityQueue()

    # initialize cost as zero
    cost = 0

    # add start state to priority queue
    priorityQ.push((root, [], cost), cost)

    # initialize current state and empty list for actions
    cur_state = None
    game_list = []

    # loop through list while it isn't empty and while it's not the goal state
    while not priorityQ.isEmpty() and not problem.isGoalState(cur_state):

        # pop state and add it to list of visited states
        cur_state, game_list, cost = priorityQ.pop()
        visitedNodes.append(cur_state)

        # for each successor, get coordinates and directions
        children = problem.getSuccessors(cur_state)
        for child in children:
            # add coordinates to visited states
            coor = child[0]
            if not coor in visitedNodes:
                # set direction, successor cost, and total cost
                d = child[1]
                child_cost = child[2]
                total_cost = cost + child_cost
                # add each child to the priority queue
                priorityQ.push((coor, game_list + [d], total_cost), total_cost)
    # return list of actions
    return game_list


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # get start state
    root = problem.getStartState()

    # create list of visited states
    closedNodes = set()

    # initialize map to keep track of distances
    g = {}
    g[root] = 0

    # create a priority queue for states 
    openNodes = util.PriorityQueue()

    # add start state w/ heuristic to priority queue
    # openNodes contains: ((state, game_list, cost), h_score)
    openNodes.push((root, [], 0), 0)

    # initialize current state and an empty list for actions
    cur_state = None
    game_list = []

    # loop through list while it isn't empty and while it's not the goal state
    while not openNodes.isEmpty() and not problem.isGoalState(cur_state):

        # pop node with lowest heuristic cost and add it to list of visited states
        cur_state, game_list, cost = openNodes.pop()
        closedNodes.add(cur_state)

        # get the successors of popped state
        children = problem.getSuccessors(cur_state)

        # for each successor, get coordinates, directions, and cost
        for child in children:
            coor = child[0]
            if not coor in closedNodes:
                d = child[1]
                child_cost = child[2]

                # check if distance from (start to current + current to child) is more than
                # distance from start to child. If so, then continue because it's not the best path.
                tentative = g[cur_state] + child_cost
                if coor in g and g[coor] < tentative:
                    continue

                g[coor] = tentative
                # add heuristic score to total travel distance from start
                h_score = g[coor] + heuristic(coor, problem)
                # add each child to the priority queue
                openNodes.push((coor, game_list + [d], child_cost), h_score)
    # return list of actions
    return game_list


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
