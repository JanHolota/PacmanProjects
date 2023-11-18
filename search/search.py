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

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    util.raiseNotDefined()"""
    "*** YOUR CODE HERE ***"
    fringe = util.Stack() ## prohledávání do hloubky využívá zásobík (LIFO)
    closed = set() ## pro ukládání rozvinutých stavů používám set, pro jeho dobré vlastnosti při testování, zda je něco prvkem setu (složitost O(1))
    fringe.push((problem.getStartState(),[])) ## přidání počátečního stavu do fringe (stav, akce vedoucí do tohoto stavu)
    while fringe.isEmpty() == False: ## cyklus trvá dokud není fringe prázdná
        position,action = fringe.pop() ## vezmu si z fringe stav(pozici) a akce vedoucí do stavu
        if problem.isGoalState(position): ## otestuji, zda je stav cílovým stavem
            return action ## pokud je cílovým stavem, vrátím list s akcemi vedoucími do stavu
        if position not in closed: ## jestliže není cílovým stavem kontrola, zda už není v closed (pokud by byl, jdu na další stav ve fringe)
            closed.add(position) ## přidám do closed
            successors = problem.getSuccessors(position) ## uložím si následníky
            for successor in successors: ## přes všechny následníky
                succIterator = iter(successor) ## zakládám iterátor přes set (successor je set)
                position = next(succIterator) ## prvním prvkem je stav
                nextAction = action + [next(succIterator)] ## druhým prvkem je akce nutná k dostání se do tohoto stavu. K ní přičtu akce všech předků
                succ = (position, nextAction) ## složím potomka pro přidání do fringe
                fringe.push(succ) ## přidám potomka do fringe
    return action ## vracím akce do posledního navštíveného uzlu, pokud nenajdu cíl

    
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    fringe = util.Queue() ## prohledávání do šířky využívá frontu (FIFO)
    closed = set() ## pro ukládání rozvinutých stavů používám set, pro jeho dobré vlastnosti při testování, zda je něco prvkem setu (složitost O(1))
    fringe.push((problem.getStartState(),[])) ## přidání počátečního stavu do fringe (stav, akce vedoucí do tohoto stavu)
    while fringe.isEmpty() == False: ## cyklus trvá dokud není fringe prázdná
        position,action = fringe.pop() ## vezmu si z fringe stav(pozici) a akce vedoucí do stavu
        if problem.isGoalState(position): ## otestuji, zda je stav cílovým stavem
            return action ## pokud je cílovým stavem, vrátím list s akcemi vedoucími do stavu
        if position not in closed: ## jestliže není cílovým stavem kontrola, zda už není v closed (pokud by byl, jdu na další stav ve fringe)
            closed.add(position) ## přidám do closed
            successors = problem.getSuccessors(position) ## uložím si následníky
            for successor in successors:  ## přes všechny následníky
                succIterator = iter(successor)  ## zakládám iterátor přes set (successor je set)
                position = next(succIterator) ## prvním prvkem je stav
                nextAction = action + [next(succIterator)] ## druhým prvkem je akce nutná k dostání se do tohoto stavu. K ní přičtu akce všech předků
                succ = (position, nextAction)  ## složím potomka pro přidání do fringe
                fringe.push(succ) ## přidám potomka do fringe
    return action ## vracím akce do posledního navštíveného uzlu, pokud nenajdu cíl

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue() ## je potřeba prvky ve fringe řadit dle ceny
    closed = set() ## pro ukládání rozvinutých stavů používám set, pro jeho dobré vlastnosti při test ování, zda je něco prvkem setu (složitost O(1)).
    fringe.push((problem.getStartState(),[],0),0) ## přidání počátečního stavu do fringe (stav, akce vedoucí do tohoto stavu,cena), cena. Dvakrát vkládám cenu, protože cema mimo set bude použita k řazení
    while fringe.isEmpty() == False: ## cyklus trvá dokud není fringe prázdná
        item = fringe.pop() ## vezmu si fringe prvek
        iterItem = iter(item) ## založím si iterátor na prvku z fringe
        position = next(iterItem)  ## vezmu si pozici
        action = next(iterItem) ## vezmu si akce
        cost = next(iterItem) ## vezmu si cenu prvku
        if problem.isGoalState(position): ## otestuji, zda je stav cílovým stavem
            return action ## vrátím akce do tohoto stavu
        if position not in closed: ## otestuji, zda není v closed
            closed.add(position) ## přidám do closed
            successors = problem.getSuccessors(position) ## uložím si následníky
            for successor in successors: ## přes všechny následníky
                succIterator = iter(successor) ## zakládám iterátor přes set (successor je set)
                position = next(succIterator) ## prvním prvkem je stav
                nextAction = action + [next(succIterator)] ## druhým prvkem je akce nutná k dostání se do stavu a přičtu akce všech předků
                nextCost = cost + next(succIterator) ## připočítám cenu předka s cenou následníka
                fringe.update((position,nextAction,nextCost),nextCost) ## použiju update (přepočítá fringe a seřadí)
    return action ## vracím akce do posledního navštíveného uzlu, pokud nenajdu cíl


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
