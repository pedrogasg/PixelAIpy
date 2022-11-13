from agents import Agent
from scene import Scene
from search import SingleSearch

class OneGoalAgent(Agent):
    def __call__(self, scene:Scene):
        search = SingleSearch(scene, tuple(scene.agent), tuple(scene.get_goals()[0]))
        path = self.path(self.fn(search))
        while path:
            p = next(path)
            yield p
