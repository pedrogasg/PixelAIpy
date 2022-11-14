from config import *
from scene import Scene
from agents import Agent
from search import AnySearch

class AnyAgent(Agent):
    def __call__(self, scene:Scene):
        xpath = []
        start_state = self.position
        goals = scene.get_goals()
        while len(goals) > 0:
            current_search = AnySearch(scene, start_state, goals)
            xpath += self.fn(current_search)
            start_state = current_search.last_state
            goals.remove(start_state)
        path = self.path(xpath)
        yield True
        while path:
            position = yield next(path)
            self.position = tuple(position)
