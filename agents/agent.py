from config import *
from scene import Scene
from search import depthFirstSearch, Search

class Agent:
    """
    This very general search agent finds a path using a supplied search
    algorithm for a supplied search problem, then play the path in the given scene
    """

    def __init__(self, shutdown, fn=depthFirstSearch) -> None:
        self.shutdown = shutdown
        self.fn = fn
        self.search = Search()

    def path(self, array):
        while array:
            yield array.pop(0)

    async def interact(self, scene:Scene):
        path = self.path(self.fn(self.search))
        while path and not self.shutdown.is_set():
            #glfw.post_empty_event()
            scene.direction_move(next(path))
            await asyncio.sleep(0.016)


