from search import Search

def depthFirstSearch(search:Search):
    """
    Search the deepest nodes in the search tree first.
    """
    start = search.start()
    stack = []
    stack.append((start, []))
    visited = set()
    while stack:
        (vertex, path) = stack.pop()
        if vertex not in visited:
            if search.goal_reached(vertex):
                return path
            visited.add(vertex)
            for neighbor in search.get_neighbors(vertex):
                stack.append((neighbor[0], path + [neighbor[1]]))

def breadthFirstSearch(search:Search):
    """
    Search the shallowest nodes in the search tree first.
    """
    start = search.start()
    queue =[]
    queue.append((start, []))
    visited = set()
    while queue:
        (vertex, path) = queue.pop(0)
        if vertex not in visited:
            if search.goal_reached(vertex):
                return path
            visited.add(vertex)
            for neighbor in search.get_neighbors(vertex):
                if neighbor[0] not in visited:
                    queue.append((neighbor[0], path + [neighbor[1]]))