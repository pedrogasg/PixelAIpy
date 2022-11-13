import agents
import search
import asyncio
from sim import Sim
from runner import Runner
from absl import app
from absl import flags
from absl import logging

FLAGS = flags.FLAGS

flags.DEFINE_integer("width", 1000, "The width size of the window")
flags.DEFINE_integer("height", 1000, "The height size of the window")
flags.DEFINE_string("layout", "smallMaze.npy", "The layout to launch")
flags.DEFINE_string("agent", "OneGoalAgent", "The name of the class of agent")
flags.DEFINE_string("function", "breadthFirstSearch", "The search function used by the agent")
flags.DEFINE_string("heuristic", "noneHeuristic", "An heuristic for the agent")

async def main(argv):
    agent_class = getattr(agents, FLAGS.agent)
    function = getattr(search, FLAGS.function)
    heuristic = getattr(search, FLAGS.heuristic)
    shutdown_event = asyncio.Event()
    myApp = Sim(FLAGS.height, FLAGS.width, True,"./layouts/" + FLAGS.layout)
    a = agent_class(function, heuristic)
    runner = Runner([a], shutdown_event)
    await asyncio.gather(
        myApp.run(shutdown_event), runner.interact(myApp.scene), return_exceptions=True
    )
    myApp.close()

def application(argv):
    asyncio.run(main(argv))

if __name__ == "__main__":
    logging.set_verbosity(logging.INFO)
    app.run(application)
    
