from config import *
from scene import Scene
from agents import Agent
from search import AnySearch

class AnyAgent(Agent):
    async def interact(self, scene:Scene):
        xpath = []
        start_state = tuple(scene.agent)
        goals = scene.get_goals()
        while len(goals) > 0:
            current_search = AnySearch(scene, start_state, goals)
            xpath += self.fn(current_search)
            start_state = current_search.last_state
            goals.remove(start_state)
        path = self.path(xpath)
        while path and not self.shutdown.is_set():
            #glfw.post_empty_event()
            scene.direction_move(next(path))
            await asyncio.sleep(0.016)
