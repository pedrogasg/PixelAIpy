from config import *

class Scene:


    def __init__(self):

        self.triangle_positions = []
        self.square_positions = []
        self.star_positions = []

        y = -.8
        while y < 1.0:
            self.triangle_positions.append(
                np.array([-0.6, y, 0], dtype = np.float32)
            )
            self.square_positions.append(
                np.array([0.0, y, 0], dtype = np.float32)
            )
            self.star_positions.append(
                np.array([0.6, y, 0], dtype = np.float32)
            )
            y += 0.2