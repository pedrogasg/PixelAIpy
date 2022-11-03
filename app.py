from config import *
import engine
import scene
import vlogging

class App:


    def __init__(self, width, height, debugMode):

        vlogging.logger.set_debug_mode(debugMode)

        self.build_glfw_window(width, height)

        #self.scene = scene.Scene.from_layout('./layouts/tiny_maze.npy')

        #self.scene = scene.Scene.from_layout('./layouts/medium_maze.npy')

        self.scene = scene.Scene.from_layout('./layouts/big_maze.npy')

        #self.scene = scene.Scene(5,10)

        self.graphicsEngine = engine.Engine(width, height, self.window, self.scene)

        self.lastTime = glfw.get_time()
        self.currentTime = glfw.get_time()
        self.numFrames = 0
        self.frameTime = 0

    def build_glfw_window(self, width, height):

        #initialize glfw
        glfw.init()

        #no default rendering client, we'll hook vulkan up to the window later
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CLIENT_API, GLFW_CONSTANTS.GLFW_NO_API)
        #resizing breaks the swapchain, we'll disable it for now
        glfw.window_hint(GLFW_CONSTANTS.GLFW_RESIZABLE, GLFW_CONSTANTS.GLFW_TRUE)
        
        #create_window(int width, int height, const char *title, GLFWmonitor *monitor, GLFWwindow *share)
        self.window = glfw.create_window(width, height, "GridWorld", None, None)
        glfw.set_window_user_pointer(self.window, self)
        glfw.set_framebuffer_size_callback(self.window, self.resize_callback)
        if self.window is not None:
            vlogging.logger.print(
                f"Successfully made a glfw window called \"GridWorld\", width: {width}, height: {height}"
            )
        else:
            vlogging.logger.print("GLFW window creation failed")

    def resize_callback(self, window, width, height):
        vkDeviceWaitIdle(self.graphicsEngine.device)
        self.graphicsEngine.recreate_swapchain(resize=True)
    
    def calculate_framerate(self):

        self.currentTime = glfw.get_time()
        delta = self.currentTime - self.lastTime

        if delta >= 1:

            framerate = max(1, int(self.numFrames // delta))
            glfw.set_window_title(self.window, f"Running at {framerate} fps.")
            self.lastTime = self.currentTime
            self.numFrames = -1
            self.frameTime = 1000.0 / framerate
        
        self.numFrames += 1

    def move_controls(self):
        if glfw.get_key(self.window, glfw.KEY_S) == glfw.PRESS:
            self.scene.move_down()
        elif glfw.get_key(self.window, glfw.KEY_W) == glfw.PRESS:
            self.scene.move_up()
        elif glfw.get_key(self.window, glfw.KEY_A) == glfw.PRESS:
            self.scene.move_left()
        elif glfw.get_key(self.window, glfw.KEY_D) == glfw.PRESS:
            self.scene.move_right()

    def depthFirstSearch(self, scene):
        """
        Search the deepest nodes in the search tree first.
        """
        i,j = scene.agent
        goal = scene.get_goals()[0]
        stack = []
        stack.append(((i,j), []))
        visited = set()
        while stack:
            (vertex, path) = stack.pop()
            
            if vertex not in visited:
                if goal[0] == vertex[0] and goal[1] == vertex[1]:
                    return path
                visited.add(vertex)
                for neighbor in scene.get_neighbors(vertex):
                    stack.append((neighbor[0], path + [neighbor[1]]))
            
    async def run(self):
        xpath = self.depthFirstSearch(self.scene)
        path = self.path(xpath)
        while not glfw.window_should_close(self.window):

            glfw.wait_events()
            self.move_controls()
            self.scene.add_state(self.scene.agent)
            self.graphicsEngine.render()
            self.calculate_framerate()
            await self.move(next(path))

    def path(self, array):
        while array:
            yield array.pop(0)
        while True:
            yield 'x'
            
    async def move(self, direction):
        self.scene.direction_move(direction)
        await asyncio.sleep(0.15)
        glfw.post_empty_event()

    async def random_move(self):
        self.scene.random_move()
        await asyncio.sleep(0.05)
        glfw.post_empty_event()

    def close(self):

        self.graphicsEngine.close()