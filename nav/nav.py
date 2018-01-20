from collections import deque, namedtuple
import heapq

from battlecode import Direction

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
        el = heapq.heappop(self.elements)
        return el[1]

def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    final_node = None

    # print([(el[0], el[1].location.x, el[1].location.y, el[1].turn)
    #        for el in frontier.elements])
    while not frontier.empty():
        current = frontier.get()
        
        if graph.success(current, goal):
            final_node = current
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + graph.heuristic(goal, next)
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
class SearchNode(namedtuple('SearchNode', ['location', 'turn', 'unit', 'heat'])):
    pass
    # def __lt__(self, other):
    #     # bc otherwise functions are compared in the priority queue
    #     if self.turn > other.turn:
    #         return False
    #     elif self.location.x > other.location.x:
    #         return False
    #     elif self.location.y > other.location.y:
    #         return False
    #     elif self.heat > other.heat:
    #         return False
    #     elif self.unit >= other.unit:
    #         return False
    #     else:
    #         return True

    # def __eq__(self, other):
    #     if not isinstance(other, SearchNode):
    #         return False
    #     return (self.location.x == other.location.x and
    #             self.location.y == other.location.y and
    #             self.turn == other.turn and
    #             self.unit == other.unit and
    #             self.heat == other.heat)

    # def __hash__(self):
    #     return hash(self.location.x ^
    #                 self.location.y ^
    #                 self.turn ^
    #                 self.unit ^
    #                 self.heat

LocationNode = namedtuple('LocationNode', ['location'])

class LocationGraph:
    '''Only tracks spatial movement (rather than time and space)'''
    def __init__(self, gc):
        self.gc = gc
    
    def neighbors(self, node):
        directions = [Direction.East,
                      Direction.North,
                      Direction.Northeast,
                      Direction.Northwest,
                      Direction.South,
                      Direction.Southeast,
                      Direction.Southwest,
                      Direction.West]
        def neighbor(d):
            return LocationNode(node.location.add(d))
        moves = [neighbor(d) for d in directions]
        filtered_moves = [m for m in moves if self.__is_clear(m)]
        return filtered_moves

    def __is_clear(self, node):
        return self.gc.is_occupiable(node.location)

    def cost(self, node1, node2):
        return (abs(node1.location.x - node2.location.x) +
                abs(node1.location.y - node2.location.y))

    def heuristic(self, node1, node2):
        x1 = node1.location.x
        y1 = node1.location.y
        x2 = node2.location.x
        y2 = node2.location.y
        return abs(x1 - x2) + abs(y1 - y2)

class SearchGraph():
    '''Tracks time, location, and heat of each unit. Allows for units to be
    routed around each other in time and space.'''
    def __init__(self, gc, nav):
        self.gc = gc
        self.nav = nav
        self.__occupations = {} # mapping of turn -> set of occupied
                                # (x, y) tuple locations

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
            def neighbor(d):
                return SearchNode(node.location.add(d),
                                  node.turn + 1,
                                  node.unit,
                                  (node.heat +
                                   self.gc.unit(node.unit).movement_cooldown() - 10))
            moves = [neighbor(d) for d in directions]
            filtered_moves = [m for m in moves if self.__is_clear(m)]
            # moves = [SearchNode(node.location.add(d),
            #                     node.turn + 1,
            #                     node.unit,
            #                     (node.heat +
            #                      self.gc.unit(node.unit).movement_cooldown() - 10))
            #          for d in directions]
            # print('all moves:', moves)
            # filtered_moves = [m for m in moves if self.__is_clear(m)]
            # print('filtered moves:', filtered_moves)
            
            return filtered_moves + [dont_move]
        else:
            #print('dont move:', dont_move)
            return [dont_move]

    def __is_clear(self, node):
        '''True iff the given node is not occupied by another unit.'''
        def check_location(location):
            if self.gc.is_occupiable(location):
                return True
            else:
                # could be occupiable later if unit is moving
                unit = self.gc.sense_unit_at_location(location)
                if unit:
                    return unit in self.nav.traveling_units.keys()
                else:
                    # print("This message should happen -- delete it later if it does")
                    return False
        
        return (check_location(node.location)
                and ((node.location.x, node.location.y) not in
                     self.occupations(node.turn)))

    def occupations(self, turn):
        # manage access to turns not in __occupations
        if turn not in self.__occupations:
            return set()
        return self.occupations(turn)

    def add_route(self, route):
        for node in route:
            if node.turn not in self.__occupations.keys():
                self.__occupations[node.turn] = set()
            
            count = len(self.__occupations[node.turn])
            self.__occupations[node.turn].add((node.location.x,
                                               node.location.y))
            if len(self.occupations(node.turn)) == count:
                print("Routed through an occupied tile!",
                      "Something's wrong with pathfinding.")

    def clear_route(self, route):
        for node in route:
            self.occupations(node.turn).remove((node.location.x, node.location.y))

    def cost(self, node1, node2):
        if node2.turn - node1.turn < 0:
            print("freak out!")
        return node2.turn - node1.turn

    def heuristic(self, goal, node2):
        x1 = goal.x
        y1 = goal.y
        x2 = node2.location.x
        y2 = node2.location.y

        h = abs(x1 - x2) + abs(y1 - y2)
        # print(x2, y2, '->', h)
        return h

    def success(self, node, goal):
        
        # TODO
        true_success = (node.location.x == goal.x and
                        node.location.y == goal.y)
        if true_success:
            return True
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
        arrived_units = []
        for id, route in self.traveling_units.items():
            unit = self.gc.unit(id)
            dest = route[-1]
            if unit.is_move_ready():
                move = route.popleft()
                dir = unit.location.map_location().direction_to(move)
                if dir is Direction.Center:
                    return
                elif self.gc.can_move(id, dir):
                    print("moving unit", id)
                    self.gc.move_robot(id, dir)
                    if unit.location.map_location() == dest:
                        print('Unit', id, 'arrived at destination', (dest.x, dest.y))
                        arrived_units.append(id)
                else:
                    print("Unit", id, "is blocked! Rerouting...")
                    self.traveling_units[id] = self.__find_route(id, dest)
        for unit in arrived_units:
            self.free_unit(unit)

    # probably only useful for testing
    def still_navigating(self):
        return not not self.traveling_units.keys()
    
    def __find_route(self, unit_id, destination):
        unit = self.gc.unit(unit_id)
        start_loc = unit.location.map_location()
        start = SearchNode(start_loc, self.gc.round(), unit_id, unit.movement_heat())
        goal = destination
        came_from, end = a_star_search(self.graph, start, goal)
        path = reconstruct_path(came_from, start, end)
        path = deque([node.location for node in path])
        # print([(l.x, l.y) for l in path])
        # self.traveling_units[unit_id] = path
        # print([(l.x, l.y) for l in path])
        # print(self.traveling_units)
        return path
        
### Backup Navigation ######################################
# TODO Idea is to keep track of total movement of units and fall back
# to decentralized control (like bug nav in an availability-first
# order) if it falls below a given threshold. Would prevent failures
# in pathfinding algorithm from screwing us.
