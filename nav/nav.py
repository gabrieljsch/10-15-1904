from collections import namedtuple
import heapq

from ..battlecode import Direction

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
    final_node = None
    
    while not frontier.empty():
        current = frontier.get()
        
        if graph.success(current, goal):
            final_node = current
            break
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current
    
    return came_from, final_node #, cost_so_far

def reconstruct_path(came_from, start, end):
    current = end
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start) # optional
    path.reverse() # optional
    return path

### Graph Implementation ###################################
SearchNode = namedtuple('SearchNode', ['location', 'turn', 'unit', 'heat'])

class SearchGraph():

    def __init__(self, gc, nav):
        self.gc = gc
        self.nav = nav
        self.occupations = {} # turn to set of occupied (x, y) tuple
                              # locations

    def neighbors(self, node):
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
                                node.heat + node.unit.movement_cooldown() - 10)
                     for d in directions
                     if self.__is_clear(node)]
            return moves + [dont_move]
        else:
            return [dont_move]

    def __is_clear(self, node):
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

    def add_route(self, route):
        for node in route:
            if not self.occupations[node.turn]:
                self.occupations[node.turn] = set()
            
            count = len(self.occupations[node.turn])
            self.occupations[node.turn].add((node.location.x,
                                             node.location.y))
            if len(self.occupations[node.turn]) == count:
                print("Routed through an occupied tile!",
                      "Something's wrong with pathfinding.")

    def clear_route(self, route):
        for node in route:
            self.occupations[node.turn].remove((node.location.x, node.location.y))

    def cost(self, node1, node2):
        return node2.turn - node1.turn

    def heuristic(self, node1, node2):
        x1 = node1.location.x
        y1 = node1.location.y
        x2 = node2.location.x
        y2 = node2.location.y
        return abs(x1 - x2) + abs(y1 - y2)

    def success(self, node, goal):
        # TODO
        true_success = (node.location.x == goal.x and
                        node.location.y == goal.y)
        if true_success:
            return true
        else:
            #if not self.__is_clear(go)
            #if not self.gc.is_occupiable(goal.location):
            return False

### Navigation Logic #######################################
# different states a unit could be in:
#  - not traveling (e.g., working, guarding, etc.)
#  - traveling
#  - trying to travel but can't find route:
#     - can get close but not all the way
#     - is stuck or blocked

class Navigator:

    # Overview of process:
    #  - maintain routes of each unit moving towards its destination
    #    and update them as necessary when things change
    #  - move units towards their dests when move_units() is called
    
    def __init__(self, gc):
        self.gc = gc
        self.graph = SearchGraph(gc, self)
        # track all units bc they are impassable
        self.units = []
        # track units that are moving and their routes
        self.traveling_units = {}
        
    def direct_unit(self, unit_id, destination):
        '''Move unit to destination over a number of turns.'''
        self.traveling_units[unit_id] = self.__find_route(unit_id, destination)
        self.units.append(unit_id)

    def free_unit(self, unit_id):
        del self.traveling_units[unit_id]

    def move_units(self):
        '''Moves all units towards their destinations.'''
        units_to_move = [u for u in self.traveling_units
                         if self.gc.unit(u).is_move_ready()]
        # figure out which units can and can't move, 
        self.traveling_units = None

    # probably only useful for testing
    def still_navigating(self):
        return not self.traveling_units
    
    def __find_route(self, unit_id, destination):
        unit = self.gc.unit(unit_id)
        start_loc = unit.location
        start = SearchNode(start_loc, self.gc.round(), unit_id, unit.movement_heat())
        goal = destination
        came_from = a_star_search(self.graph, start, goal)
        path = reconstruct_path(came_from, start, end)
        print(path)
        
### Backup Navigation ######################################
# TODO Idea is to keep track of total movement of units and fall back
# to decentralized control (like bug nav in an availability-first
# order) if it falls below a given threshold. Would prevent failures
# in pathfinding algorithm from screwing us.

print('ran')
