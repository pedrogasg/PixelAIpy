from config import *

class Agent:
    def __init__(self, shutdown) -> None:
        self.shutdown = shutdown

    def path(self, array):
        while array:
            yield array.pop(0)

    async def interact(self, scene):

        path = self.path(self.breadthFirstSearch(scene=scene))

        while path and not self.shutdown.is_set():
            #glfw.post_empty_event()
            scene.direction_move(next(path))
            await asyncio.sleep(0.016)
    
    def depthFirstSearch(self, scene):
        """
        Search the deepest nodes in the search tree first.
        """
        i,j = scene.agent
        goal = scene.get_goals()[0]
        stack = []
        stack.append(((i,j), []))
        visited = set()
        while stack:
            (vertex, path) = stack.pop()
            
            if vertex not in visited:
                if goal[0] == vertex[0] and goal[1] == vertex[1]:
                    return path
                visited.add(vertex)
                for neighbor in scene.get_neighbors(vertex):
                    stack.append((neighbor[0], path + [neighbor[1]]))

    def breadthFirstSearch(self, scene):
        """
        Search the shallowest nodes in the search tree first.
        """
        i,j = scene.agent
        goal = scene.get_goals()[0]
        queue =[]
        queue.append(((i,j), []))
        visited = set()
        while queue:
            (vertex, path) = queue.pop(0)
            if goal[0] == vertex[0] and goal[1] == vertex[1]:
                return path
            for neighbor in scene.get_neighbors(vertex):
                if neighbor[0] not in visited:
                    visited.add(neighbor[0])
                    queue.append((neighbor[0], path + [neighbor[1]]))