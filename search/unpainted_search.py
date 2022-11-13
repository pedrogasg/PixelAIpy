from search import Search
from scene import Scene
from bitarray.util import zeros, ba2int, int2ba

class UnpaintedSearch(Search):
    def __init__(self, scene:Scene, cost_fn=lambda n:1) -> None:
        self.scene = scene
        self._start = tuple(scene.agents[0])
        self._goals = scene.get_goals()
        self._goals_lenght = len(self._goals)
        self._reached = zeros(self._goals_lenght)
        self.cost = cost_fn

    def start(self):
        return self._start, ba2int(self._reached)

    def get_neighbors(self, state):
        vertex, reached = state
        bynary = int2ba(reached, self._goals_lenght)
        neighbors = self.scene.get_neighbors(vertex)
        successors = []
        for n, p in neighbors:
            if n in self._goals:
                r = bynary.copy()
                index = self._goals.index(n)
                r[index] = 1
                successors.append(((n, ba2int(r)), p))
            else:
                successors.append(((n, reached), p))
        return [(n, p, self.cost(n)) for n, p in successors]

    def goal_reached(self, state):
        vertex, reached = state
        bynary = int2ba(reached, self._goals_lenght)
        return bynary.all()