from config import *
from scene import Scene
from search import depthFirstSearch, Search

class Agent:
    """
    This very general search agent finds a path using a supplied search
    algorithm for a supplied search problem, then play the path in the given scene
    """

    def __init__(self, fn=depthFirstSearch, heur=None) -> None:
        if heur is not None:
            self.fn = lambda x: fn(x, heur)
        else:
            self.fn = fn

    def __call__(self, scene:Scene):
        raise NotImplemented
        

    def path(self, array):
        while array:
            yield array.pop(0)



