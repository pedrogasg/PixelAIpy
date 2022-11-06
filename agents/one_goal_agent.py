from agents import Agent
from scene import Scene
from search import SingleSearch

class OneGoalAgent(Agent):
    async def interact(self, scene:Scene):
        self.search = SingleSearch(scene, tuple(scene.agent), tuple(scene.get_goals()[0]))
        await super().interact(scene=scene)
