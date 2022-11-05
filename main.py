import app
import agent

import asyncio

async def main():
    shutdown_event = asyncio.Event()
    myApp = app.App(800, 800, True)
    a = agent.Agent(shutdown_event)
    await asyncio.gather(
        myApp.run(shutdown_event),
        a.interact(myApp.scene),
        return_exceptions=True
    )
    myApp.close()

if __name__ == "__main__":

    asyncio.run(main())