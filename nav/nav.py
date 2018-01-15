import heapq

# high level overview:
#  - use a pathfinding algo as a black box
#  - detect getting stuck, reroute
#  - coordinate movement between multiple bots (direct them one by one, parametrically)
# problems:
#  - detecting new obstacles/enemy movement and rerouting appropriately

### Graph Search ###########################################

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        
        if graph.success(current, goal):
            break
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current
    
    return came_from, cost_so_far

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start) # optional
    path.reverse() # optional
    return path

### Graph Implementation ###################################

SearchNode = namedTuple('SearchNode', ['location', 'turn', 'unit', 'heat'])

class SearchGraph():

    def __init__(self, gc, nav):
        self.gc = gc
        self.nav = nav
        self.occupations = {} # turn to set of occupied (x, y) tuple
                              # locations

    def neighbors(node):
        dont_move = SearchNode(node.location, node.turn+1, node.unit,
                               max(node.heat - 10, 0))
        # unit can move:
        if node.heat < 10:
            directions = [Direction.East,
                          Direction.North,
                          Direction.Northeast,
                          Direction.Northwest,
                          Direction.South,
                          Direction.Southeast,
                          Direction.Southwest,
                          Direction.West]
            moves = [SearchNode(node.location.add(d),
                                node.turn + 1,
                                node.unit,
                                node.heat + node.unit.movement_cooldown())
                     for d in directions
                     if self.__is_clear(node)]
            return moves + [dont_move]
        else:
            return [dont_move]

    def __is_clear(node):
        '''True iff the given node is not occupied by another unit.'''
        def check_location(location):
            if self.gc.is_occupiable(node.location):
                return True
            else:
                # could be occupiable later if unit is moving
                unit = self.gc.sense_unit_at_location(location)
                if unit:
                    return unit.id in nav.traveling_units
                else:
                    print("This message should happen -- delete it later if it does")
                    return False
        
        return (check_location(node.location)
                and ((node.location.x, node.location.y) not in
                     self.occupations[node.turn]))

    def add_route(route):
        for node in route:
            if not self.occupations[node.turn]:
                self.occupations[node.turn] = set()
            
            count = len(self.occupations[node.turn])
            self.occupations[node.turn].add((node.location.x,
                                             node.location.y))
            if len(self.occupations[node.turn]) == count:
                print("Routed through an occupied tile!",
                      "Something's wrong with pathfinding.")

    def clear_route(route):
        for node in route:
            self.occupations[node.turn].remove((node.location.x, node.location.y))

    def cost(node1, node2):
        return node2.turn - node1.turn

    def heuristic(node1, node2):
        x1 = node1.location.x
        y1 = node1.location.y
        x2 = node2.location.x
        y2 = node2.location.y
        return abs(x1 - x2) + abs(y1 - y2)

    def success(node, goal):
        return (node.location.x == goal.location.x and
                node.location.y == goal.location.y)

### Navigation Logic #######################################
    
class Navigator:

    # Overview of process:
    #  - maintain routes of each unit moving towards its destination
    #    and update them as necessary when things change
    #  - move units towards their dests when move_units() is called
    
    def __init__(self, gc):
        self.gc = gc
        self.searchGraph = SearchGraph(gc, self)
        # track all units bc they are impassable
        self.units = []
        # track units that are moving and their routes
        self.traveling_units = {}
        
    def direct_unit(unit, destination):
        '''Move unit to destination over a number of turns.'''
        self.traveling_units[unit.id] = None # TODO
        self.units.append(unit.id)

    def free_unit(unit):
        del self.traveling_units[unit.id]

    def move_units():
        '''Moves all units towards their destinations.'''
        units_to_move = [u for u in self.traveling_units if u.is_move_ready()]
        pass
        
    def __route_unit(unit):
        
