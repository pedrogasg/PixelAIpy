from search import Search

def depthFirstSearch(search:Search):
    """
    Search the deepest nodes in the search tree first.
    """
    start = search.start()
    stack = []
    stack.append((start, [], 0))
    visited = set()
    print("We are figthing heros")
    while stack:
        (vertex, path, cost) = stack.pop()
        if vertex not in visited:
            if search.goal_reached(vertex):
                return path
            visited.add(vertex)
            for neighbor, direction, n_cost in search.get_neighbors(vertex):
                stack.append((neighbor, path + [direction], cost + n_cost))

def breadthFirstSearch(search:Search):
    """
    Search the shallowest nodes in the search tree first.
    """
    start = search.start()
    queue =[]
    queue.append((start, [], 0))
    visited = set()
    while queue:
        (vertex, path, cost) = queue.pop(0)
        if vertex not in visited:
            if search.goal_reached(vertex):
                return path
            visited.add(vertex)
            for neighbor, direction, n_cost in search.get_neighbors(vertex):
                if neighbor not in visited:
                    queue.append((neighbor, path + [direction], cost + n_cost))