from agents import Agent
from scene import Scene
from search import SingleSearch

class OneGoalAgent(Agent):
    def __call__(self, scene:Scene):
        search = SingleSearch(scene, self.position, tuple(scene.get_goals()[0]))
        path = self.path(self.fn(search))
        yield True
        while path:
            p = next(path)
            position = yield p
            self.position = tuple(position)
