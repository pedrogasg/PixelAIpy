import asyncio
from scene import Scene
class Runner:
    def __init__(self, agents, shutdown) -> None:
        self.agents = agents
        self.shutdown = shutdown

    async def interact(self, scene:Scene):
        actions = [agent(scene) for agent in self.agents]
        positions = [agent.agent for agent in self.agents]
        for action in actions:
            next(action)
        while not self.shutdown.is_set():
            #glfw.post_empty_event()
            for i, action in enumerate(actions):
                direction = action.send(positions[i])
                p = scene.direction_move(direction, i)
                positions[i] = p
                await asyncio.sleep(0.016)