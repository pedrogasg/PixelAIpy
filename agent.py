from config import *
from scene import Scene
from search import breadthFirstSearch, depthFirstSearch, Search

class SingleSearch(Search):
    def __init__(self, scene:Scene, start, goal) -> None:
        self.scene = scene
        self._start = start
        self._goal = goal
        self.search = Search()

    def start(self):
        return self._start

    def get_neighbors(self, state):
        return self.scene.get_neighbors(state)

    def goal_reached(self, state):
        return self._goal == state

class Agent:
    def __init__(self, shutdown) -> None:
        self.shutdown = shutdown

    def path(self, array):
        while array:
            yield array.pop(0)

    async def interact(self, scene:Scene):
        path = self.path(depthFirstSearch(self.search))
        while path and not self.shutdown.is_set():
            #glfw.post_empty_event()
            scene.direction_move(next(path))
            await asyncio.sleep(0.016)


class OneGoalAgent(Agent):
    async def interact(self, scene:Scene):
        self.search = SingleSearch(scene, tuple(scene.agent), tuple(scene.get_goals()[0]))
        await super().interact(scene=scene)
