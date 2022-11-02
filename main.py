import app

import asyncio

if __name__ == "__main__":

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    myApp = app.App(800, 800, True)

    loop.run_until_complete(myApp.run())
    
    myApp.close()
    loop.close()