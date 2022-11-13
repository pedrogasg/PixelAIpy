from agents import Agent
from scene import Scene
from search import UnpaintedSearch

class UnpaintedAgent(Agent):
    def __call__(self, scene:Scene):
        search = UnpaintedSearch(self.agent, scene)
        path = self.path(self.fn(search))
        yield True
        while path:
            agent = yield next(path)
            self.agent = tuple(agent)
