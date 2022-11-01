from config import *

class Scene:
    def __init__(self, height, width):
        self.dirty = False

        self.vertex_size = 8
        self.vertices = np.zeros(height * width * self.vertex_size, dtype = np.float32)
        size = 2. / height
        self.size = [size]
        for i in range(height):

            for j in range(width):
                position = (((i * height)) + j) * self.vertex_size
                self.vertices[position] = (i * size) - ((height / 2.) * size)
                self.vertices[position + 1] = (j * size) - ((width / 2.) * size)
                self.vertices[position + 2] = i
                self.vertices[position + 3] = j

        self.agent = [3,0]

        self.color = [0.9, 0.9, 0.9, 0.5]

        self.push_constant_size = len(self.push_constant[0])

        self.height = height
        self.width = width
        self.world_state = np.random.choice([0,1],(height,width), p=[0.1,0.9])
        self.world_actions = np.pad(self.world_state,1)

        xs, ys = np.where(self.world_state == 0)
        for x, y in zip(xs, ys):
            position = (((x * height)) + y) * self.vertex_size
            self.vertices[position + 4] = 1

    @property
    def actions(self):
        indices = ((self.agent[0],self.agent[0]+2,self.agent[0]+1,self.agent[0]+1),(self.agent[1]+1,self.agent[1]+1,self.agent[1],self.agent[1]+2))
        return self.world_actions[indices]


    @property
    def push_constant(self):
        return [self.color + self.agent + self.size]

    def add_state(self, state):
        
        position = (((state[0] * self.height)) + state[1]) * self.vertex_size
        #self.world_state[state[0],state[1]] = 0
        #self.world_actions[state[0]+1,state[1]+1] = 0
        self.vertices[position + 5] = 1
        self.dirty = True
    

    def move_down(self):
        self.agent = [self.agent[0], self.agent[1] + self.actions[3]]
       
    def move_up(self):
        self.agent = [self.agent[0], self.agent[1] - self.actions[2]]
    def move_left(self):
        self.agent = [self.agent[0] - self.actions[0], self.agent[1] ]

    def move_right(self):
        self.agent = [self.agent[0] + self.actions[1], self.agent[1]]