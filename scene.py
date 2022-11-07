from config import *

class Scene:

    @classmethod
    def from_layout(cls, filepath):
        with open(filepath, 'rb') as f:
            state = np.load(f)

        h, w = state.shape

        return cls(h,w,state)


    def __init__(self, height, width, state=None):
        self.dirty = False

        self.vertex_size = 8
        self.vertices = np.zeros(height * width * self.vertex_size, dtype = np.float32)
        size_h = 2. / height
        size_w = 2. / width
        self.size = [size_w, size_h]
        for i in range(height):

            for j in range(width):
                position = ((i * width) + j) * self.vertex_size
                self.vertices[position] = (j * size_w) - ((width / 2.) * size_w)
                self.vertices[position + 1] = (i * size_h) - ((height / 2.) * size_h)
                self.vertices[position + 2] = j
                self.vertices[position + 3] = i


        self.color = [0.9, 0.9, 0.9, 0.5]


        self.height = height
        self.width = width
        if state is None:
            self.world_state = np.random.choice([0,1],(height,width), p=[0.15,0.85]) # np.ones((height, width), dtype=int) # np.random.choice([0,1],(height,width), p=[0.1,0.9])
            self.painted_state = np.copy(self.world_state)
            xs, ys = np.where(self.world_state == 1)
            self.agent = [xs[0],ys[0]]
            self.goals =  [(x, y) for x, y in zip(xs,ys)]
        else:
            world_state = np.ones((height, width), dtype=int)
            world_state[np.where(state == 0)] = 0
            self.world_state = world_state
            self.painted_state = np.copy(self.world_state)
            xs, ys = np.where(state == -1)
            self.agent = [xs[0],ys[0]]
            self.update_vertices(state, 2, 5, self.painted_state)
            xs, ys = np.where(state == 1)
            self.goals =  [(x, y) for x, y in zip(xs,ys)]

            
        self.world_actions = np.pad(self.world_state,1)

        self.update_vertices(self.world_state, 0, 4)
            
        self.push_constant_size = len(self.push_constant[0])

        self.movement_set = { 'down':self.move_down, 'up':self.move_up, 'left':self.move_left, 'right':self.move_right}

    @property
    def actions(self):
        indices = ((self.agent[0],self.agent[0]+2,self.agent[0]+1,self.agent[0]+1),(self.agent[1]+1,self.agent[1]+1,self.agent[1],self.agent[1]+2))
        return self.world_actions[indices]


    @property
    def push_constant(self):
        return [self.color + self.agent + self.size]

    def update_vertices(self, world_state, lookfor, offset, with_state=None):
        xs, ys = np.where(world_state == lookfor)
        for x, y in zip(xs, ys):
            position = (((x * self.width)) + y) * self.vertex_size
            self.vertices[position + offset] = 1
        if with_state is not None:
            with_state[(xs, ys)] = 0

    def add_state(self, state):
        position = (((state[0] * self.width)) + state[1]) * self.vertex_size
        self.painted_state[state[0],state[1]] = 0
        #self.world_state[state[0],state[1]] = 0
        #self.world_actions[state[0]+1,state[1]+1] = 0
        self.vertices[position + 5] = 1
        self.dirty = True

    def get_goals(self):
        xs, ys = np.where(self.painted_state == 1) 
        return [(x, y) for x, y in zip(xs,ys)]

    def get_neighbors(self, vertice):
        indices = ((vertice[0],vertice[0]+2,vertice[0]+1,vertice[0]+1),(vertice[1]+1,vertice[1]+1,vertice[1],vertice[1]+2))
        actions = self.world_actions[indices]
        indices = ((vertice[0]-1,vertice[0]+1,vertice[0],vertice[0]),(vertice[1],vertice[1],vertice[1]-1,vertice[1]+1))
        moves = 'up', 'down', 'left', 'right'
        return [((i,j),m) for i, j, a, m in zip(indices[0], indices[1], actions, moves) if a > 0]

    def move_right(self):
        self.agent = [self.agent[0], self.agent[1] + self.actions[3]]
       
    def move_left(self):
        self.agent = [self.agent[0], self.agent[1] - self.actions[2]]
    
    def move_up(self):
        self.agent = [self.agent[0] - self.actions[0], self.agent[1] ]

    def move_down(self):
        self.agent = [self.agent[0] + self.actions[1], self.agent[1]]
    
    def direction_move(self, direction):
        if direction in self.movement_set:
            self.movement_set[direction]()

    def random_move(self):
        movent_set = [self.move_down, self.move_up, self.move_left, self.move_right]
        direction = np.random.choice(range(4))
        movent_set[direction]()