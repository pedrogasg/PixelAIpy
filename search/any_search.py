from search import Search
from scene import Scene

class AnySearch(Search):
    def __init__(self, scene:Scene, start, goals, cost_fn=lambda n:1) -> None:
        self.scene = scene
        self.cost = cost_fn
        self._start = start
        self.last_state = start
        self._goal = start
        self.goals = goals

    def start(self):
        return self._start

    def get_neighbors(self, state):
        return [(n, p, self.cost(n)) for n, p in self.scene.get_neighbors(state)]

    def goal_reached(self, state):
        if state in self.goals:
            self.last_state = state
            return True
        return False