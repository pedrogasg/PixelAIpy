from search import SingleSearch, UnpaintedSearch
from bitarray.util import int2ba

nullHeuristic = lambda p, s: 0

def manhattanHeuristic(position, search:SingleSearch, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = search._goal
    return manhattanDistance(xy1, xy2)

def euclideanHeuristic(position, search:SingleSearch, info={}):
    "The Euclidean distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = search._goal
    return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5


def unPaintedInconsistentHeuristic(state, search:UnpaintedSearch):

    position, unpainted = state
    
    if search.goal_reached(state):
        return 0
    unpainted_wall = []
    bynary = int2ba(unpainted, search._goals_lenght)
    for i, b in enumerate(bynary):
        if b == 0:
            unpainted_wall.append(search._goals[i])

    current_pos = position
    total_cost = 0
    while len(unpainted_wall) != 0:
        i, dist = upper_Distance(current_pos, unpainted_wall)
        total_cost += dist
        current_pos = unpainted_wall[i]
        unpainted_wall.remove(unpainted_wall[i])
    return total_cost



def upper_Distance(actual_pos, corners):
	index = -1
	maxi = 0
	for i in range(len(corners)):
		dist = manhattanDistance(actual_pos, corners[i])
		if maxi == 0 or maxi < dist:
			index = i
			maxi = dist
	return index, maxi

def manhattanDistance(xy1, xy2):
    "The Manhattan distance"

    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])