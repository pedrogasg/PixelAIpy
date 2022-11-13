import asyncio
from scene import Scene
class Runner:
    def __init__(self, agents, shutdown) -> None:
        self.agents = agents
        self.shutdown = shutdown

    async def interact(self, scene:Scene):
        while not self.shutdown.is_set():
            #glfw.post_empty_event()
            for i, agent in enumerate(self.agents):
                action = next(agent(scene))
                scene.direction_move(action, i)
                await asyncio.sleep(0.016)