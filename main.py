from app import App
from agents import OneGoalAgent, UnpaintedAgent, AnyAgent
from search import (
    breadthFirstSearch,
    depthFirstSearch,
    uniformCostSearch,
    greedySearch,
    aStarSearch,
    manhattanHeuristic,
    unPaintedInconsistentHeuristic
)


import asyncio


async def main():
    shutdown_event = asyncio.Event()
    myApp = App(1000, 1000, True)
    #a = OneGoalAgent(shutdown_event, greedySearch, manhattanHeuristic)
    #a = UnpaintedAgent(shutdown_event, aStarSearch, unPaintedInconsistentHeuristic)
    #a = AnyAgent(shutdown_event, breadthFirstSearch)
    #a = AnyAgent(shutdown_event, depthFirstSearch)
    a = AnyAgent(shutdown_event, greedySearch, manhattanHeuristic)
    #a = AnyAgent(shutdown_event, aStarSearch, manhattanHeuristic)
    #a = AnyAgent(shutdown_event, uniformCostSearch)
    await asyncio.gather(
        myApp.run(shutdown_event), a.interact(myApp.scene), return_exceptions=True
    )
    myApp.close()


if __name__ == "__main__":

    asyncio.run(main())
