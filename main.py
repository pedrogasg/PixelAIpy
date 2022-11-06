from app import App
from agents import OneGoalAgent

import asyncio

async def main():
    shutdown_event = asyncio.Event()
    myApp = App(800, 800, True)
    a = OneGoalAgent(shutdown_event)
    await asyncio.gather(
        myApp.run(shutdown_event),
        a.interact(myApp.scene),
        return_exceptions=True
    )
    myApp.close()

if __name__ == "__main__":

    asyncio.run(main())