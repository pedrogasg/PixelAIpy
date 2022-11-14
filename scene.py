from config import *

class Scene:

    @classmethod
    def from_layout(cls, filepath):
        with open(filepath, 'rb') as f:
            state = np.load(f)

        h, w = state.shape
        return cls(h,w,state)

    def __init__(self, height, width, state=None):

        self.inititialize(height, width)

        for i in range(height):

            for j in range(width):
                position = ((i * width) + j) * self.vertex_size
                self.populate(self.vertices, j, i, position)

        if state is None:
            self.init_random()
        else:
            self.init_from_state(state)
            
        self.world_actions = np.pad(self.world_state,1)

        self.update_vertices(self.world_state, 0, 4)
            
        self.push_constant_size = len(self.push_constant[0])

        self.movement_set = { 'down':self.move_down, 'up':self.move_up, 'left':self.move_left, 'right':self.move_right}

    def inititialize(self, height, width):
        self.dirty = False
        self.vertex_size = 8
        self.vertices = np.zeros(height * width * self.vertex_size, dtype = np.float32)
        self.height = height
        self.width = width
        size_h = 2. / height
        size_w = 2. / width
        self.size = [size_w, size_h]
        self.color = [0.9, 0.9, 0.9, 0.5]
        self.agents_positions = []
        self.agents_vertex = np.array([],dtype=np.float32)

    def init_random(self):
        self.world_state = np.random.choice([0,1],(self.height,self.width), p=[0.15,0.85]) # np.ones((height, width), dtype=int) # np.random.choice([0,1],(height,width), p=[0.1,0.9])
        self.painted_state = np.copy(self.world_state)
        xs, ys = np.where(self.world_state == 1)
        self.agents_positions.append(self.create_agent([xs[0],ys[0]]))
        self.goals =  [(x, y) for x, y in zip(xs,ys)]

    def init_from_state(self, state):
        world_state = np.ones((self.height, self.width), dtype=int)
        world_state[np.where(state == 0)] = 0
        self.world_state = world_state
        self.painted_state = np.copy(self.world_state)
        xs, ys = np.where(state == -1)
        for x, y in zip(xs, ys):
            self.agents_positions.append(self.create_agent(x, y))
        self.update_vertices(state, 2, 5, self.painted_state)
        xs, ys = np.where(state == 1)
        self.goals =  [(x, y) for x, y in zip(xs,ys)]

    def actions(self, agent_index):
        agent = self.agents_positions[agent_index]
        indices = ((agent[0],agent[0]+2,agent[0]+1,agent[0]+1),(agent[1]+1,agent[1]+1,agent[1],agent[1]+2))
        return self.world_actions[indices]

    def create_agent(self, x, y):
        agent = np.zeros(self.vertex_size, dtype = np.float32)
        self.populate(agent, x, y, len(self.agents_positions))
        agent[4] = 2.
        self.agents_vertex = np.append(self.agents_vertex, agent)
        return [x, y]

    def position(self, pos):
        x, y = pos
        size_w, size_h = self.size
        x_ = (x * size_w) - ((self.width / 2.) * size_w)
        y_ = (y * size_h) - ((self.height / 2.) * size_h)
        return x_, y_

    def populate(self, vertices, x, y, position):
        x_, y_ = self.position((x, y))
        vertices[position] = x_
        vertices[position + 1] = y_
        vertices[position + 2] = x
        vertices[position + 3] = y

    @property
    def push_constant(self):
        return [self.color + [0,0] + self.size]

    def get_push_constant(self, position):
        return [[1., 0.6, 0.0, 1.] + position + self.size]

    def update_vertices(self, world_state, lookfor, offset, with_state=None):
        xs, ys = np.where(world_state == lookfor)
        for x, y in zip(xs, ys):
            position = (((x * self.width)) + y) * self.vertex_size
            self.vertices[position + offset] = 1
        if with_state is not None:
            with_state[(xs, ys)] = 0

    def add_state(self):
        for agent in self.agents_positions:
            if self.painted_state[agent[0],agent[1]] != 0:
                position = (((agent[0] * self.width)) + agent[1]) * self.vertex_size
                self.painted_state[agent[0],agent[1]] = 0
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

    def move_right(self, agent, actions):
        x, y = agent
        return [x, y + actions[3]]
       
    def move_left(self, agent, actions):
        x, y = agent
        return [x, y - actions[2]]
    
    def move_up(self, agent, actions):
        x, y = agent
        return [x - actions[0], y ]

    def move_down(self, agent, actions):
        x, y = agent
        return [x + actions[1], y]
    
    def direction_move(self, direction, agent_index):
        actions = self.actions(agent_index)
        agent = self.agents_positions[agent_index]
        if direction in self.movement_set:
            new_agent = self.movement_set[direction](agent, actions)
            self.agents_positions[agent_index] = new_agent
            return new_agent
        else:
            return agent

    def random_move(self, agent_index):
        actions = self.actions(agent_index)
        agent = self.agents_positions[agent_index]
        direction = np.random.choice(self.movement_set.keys)
        new_agent = self.movement_set[direction](agent, actions)
        self.agents_positions[agent_index] = new_agent
        return new_agent