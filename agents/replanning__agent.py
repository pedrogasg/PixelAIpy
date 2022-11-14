from config import *
from scene import Scene
from agents import Agent
from search import AnySearch

class ReplanningAgent(Agent):
    def __call__(self, scene:Scene):
        goals = scene.get_goals()
        yield True
        while len(goals) > 0:
            current_search = AnySearch(scene, self.position, goals)
            xpath = self.fn(current_search)
            path = self.path(xpath)
            for value in path:
                position = yield value
                self.position = tuple(position)
            goals.remove(self.position)
