from config import *
from render import Engine
import math
import scene
import vlogging

class Sim:


    def __init__(self, width, height, debugMode, layout):

        vlogging.logger.set_debug_mode(debugMode)

        self.scene = scene.Scene.from_layout(layout)
        max_scene = max(self.scene.height, self.scene.width)
        max_window = max(height, width)
        denominator = max_window // max_scene
        height = int(self.scene.height * denominator)
        width = int(self.scene.width * denominator)
        self.build_glfw_window(width, height)

        self.graphicsEngine = Engine(width, height, self.window, self.scene)

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


            
    async def run(self, shutdown):

        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            #glfw.wait_events()
            self.move_controls()
            self.scene.add_state()
            self.graphicsEngine.render()
            self.calculate_framerate()
            await asyncio.sleep(0)

        shutdown.set()


            

    def close(self):

        self.graphicsEngine.close()