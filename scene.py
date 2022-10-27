from config import *

class Scene:
    def __init__(self, height, width):
        vertex_size = 6
        self.vertices = np.ones(height * width * vertex_size, dtype = np.float32)
        size = 2. / height
        for i in range(height):

            for j in range(width):
                position = (((i * height)) + j) * vertex_size
                self.vertices[position] = (i * size) - ((height / 2.) * size)
                self.vertices[position + 1] = (j * size) - ((width / 2.) * size)



        self.color = [[0.9, 0.9, 0.9, 0.5]]



        # self.vertices = np.array(
        #     (0.0, 0.5, 0.0, 1.0, 0.0, 0.0,
        #      0.5, 0.0, 0.0, 1.0, 0.0, 0.0,
        #     -0.5, 0.0, 0.0, 1.0, 0.0, 0.0), dtype = np.float32
        # )
