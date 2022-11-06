from search import Search
from scene import Scene

class SingleSearch(Search):
    def __init__(self, scene:Scene, start, goal, cost_fn=lambda n:1) -> None:
        self.scene = scene
        self._start = start
        self._goal = goal
        self.cost = cost_fn

    def start(self):
        return self._start

    def get_neighbors(self, state):
        return [(n, p, self.cost(n)) for n, p in self.scene.get_neighbors(state)]

    def goal_reached(self, state):
        return self._goal == state