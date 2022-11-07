from agents import Agent
from scene import Scene
from search import UnpaintedSearch

class UnpaintedAgent(Agent):
    async def interact(self, scene:Scene):
        self.search = UnpaintedSearch(scene)
        await super().interact(scene=scene)
