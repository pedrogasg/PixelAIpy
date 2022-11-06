from search import Search
from tools import Stack, Queue, PriorityQueue

def depthFirstSearch(search:Search):
    """
    Search the deepest nodes in the search tree first.
    """
    start = search.start()
    stack = Stack()
    stack.push((start, [], 0))
    visited = set()
    print("We are figthing heros")
    while stack:
        (vertex, path, cost) = stack.pop()
        if vertex not in visited:
            if search.goal_reached(vertex):
                return path
            visited.add(vertex)
            for neighbor, direction, n_cost in search.get_neighbors(vertex):
                stack.push((neighbor, path + [direction], cost + n_cost))

def breadthFirstSearch(search:Search):
    """
    Search the shallowest nodes in the search tree first.
    """
    start = search.start()
    queue = Queue()
    queue.push((start, [], 0))
    visited = set()
    while queue:
        (vertex, path, cost) = queue.pop()
        if vertex not in visited:
            if search.goal_reached(vertex):
                return path
            visited.add(vertex)
            for neighbor, direction, n_cost in search.get_neighbors(vertex):
                if neighbor not in visited:
                    queue.push((neighbor, path + [direction], cost + n_cost))

def uniformCostSearch(search:Search):
    """Search the node of least total cost first."""
    start = search.start()
    queue = PriorityQueue()
    queue.push((start,[], 0),1)
    visited = set()
    while queue:
        (vertex, path, cost) = queue.pop()
        if vertex not in visited:
            if search.goal_reached(vertex):
                return path
            visited.add(vertex)
            for neighbor, direction, n_cost in search.get_neighbors(vertex):
                if neighbor not in visited:
                    queue.push((neighbor, path + [direction], cost + n_cost), cost + n_cost)

def aStarSearch(search:Search, heuristic=lambda x,s: 0):
    """Search the node that has the lowest combined cost and heuristic first."""
    start = search.start()
    queue = PriorityQueue()
    queue.push((start,[], 0),1)
    visited = set()
    while queue:
        (vertex, path, cost) = queue.pop()
        if vertex not in visited:
            if search.goal_reached(vertex):
                return path
            visited.add(vertex)
            for neighbor, direction, n_cost in search.get_neighbors(vertex):
                if neighbor not in visited:
                    h = heuristic(neighbor, search)
                    queue.push((neighbor, path + [direction], cost + n_cost), h + cost + n_cost)

def greedySearch(search:Search, heuristic=lambda x,s: 0):
    """Search the node that has the lowest heuristic first."""
    start = search.start()
    queue = PriorityQueue()
    queue.push((start,[], 0),1)
    visited = set()
    while queue:
        (vertex, path, cost) = queue.pop()
        if vertex not in visited:
            if search.goal_reached(vertex):
                return path
            visited.add(vertex)
            for neighbor, direction, n_cost in search.get_neighbors(vertex):
                if neighbor not in visited:
                    h = heuristic(neighbor, search)
                    queue.push((neighbor, path + [direction], cost + n_cost), h)
