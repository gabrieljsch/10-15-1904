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
    path.append(start) # optional # TODO should this be here?
    path.reverse() # optional
    return path

# cycle detection
def cyclic(graph):
    """Return True if the directed graph has a cycle.
    The graph must be represented as a dictionary mapping vertices to
    iterables of neighbouring vertices. For example:

    >>> cyclic({1: (2,), 2: (3,), 3: (1,)})
    True
    >>> cyclic({1: (2,), 2: (3,), 3: (4,)})
    False

    """
    visited = set()
    path = [object()]
    path_set = set(path)
    stack = [iter(graph)]
    while stack:
        for v in stack[-1]:
            if v in path_set:
                return True
            elif v not in visited:
                visited.add(v)
                path.append(v)
                path_set.add(v)
                stack.append(iter(graph.get(v, ())))
                break
        else:
            path_set.remove(path.pop())
            stack.pop()
    return False

### Graph Implementation ###################################

LocationNode = namedtuple('LocationNode', ['location'])
class ScoutGraph:
    '''For scouting if a route exists and ordering unit routing. Only
    tracks spatial movement (rather than time and space)'''
    def __init__(self, gc, unit_id, deps, continuation):
        self.gc = gc
        self.unit_id = unit_id
        self.deps = deps
        # Passed in to allow units to be routed as they're
        # encountered. Takes 3 parameters: the unit whose path is
        # being scouted, the unit that is encountered, and a
        # dependency graph. Dependency graph is a dict representation
        # of graph where unit 1 has an edge to unit 2 if unit 1's
        # movement depends on the movement of unit 2.

        # continuation(unit, other_unit, deps)
        self.continuation = continuation
    
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
        # idea: if the blocking unit is a friendly one, add this unit
        # to some queue to be processed after that unit moves
        
        if self.gc.is_occupiable(node.location):
            return True
        else:
            # option 1: if we encounter a unit that is traveling or
            # not yet assigned, assume it doesn't block us.

            # The difference between these options is the order in
            # which units are processed -- this is pretty important
            # unit = self.gc.sense_unit_ate_location(location)
            # if unit:
            #     return True
            
            # option 2: if we encounter a unit that is not yet routed,
            # route it. Then, treat this tile as though it is occupiable.

            # Idea: opt 2 but keep track of dependencies between units
            # better idea: opt 2 but only route that unit if we fail
            other_unit = self.gc.sense_unit_at_location(node.location)
            if other_unit is not None:
                # print('found unit', other_unit)
                return self.continuation(self.unit_id, other_unit, self.deps)
            else:
                # print("This message should happen -- delete it later if it does")
                return False
        
        return 

    def cost(self, node1, node2):
        return 1
        # return (abs(node1.location.x - node2.location.x) +
        #         abs(node1.location.y - node2.location.y))

    def heuristic(self, node1, node2):
        x1 = node1.location.x
        y1 = node1.location.y
        x2 = node2.location.x
        y2 = node2.location.y
        return abs(x1 - x2) + abs(y1 - y2)

    def success(self, node, goal):    
        return node.location == goal.location



SearchNode = namedtuple('SearchNode', ['location', 'turn', 'unit', 'heat'])

class SearchGraph():
    '''Tracks time, location, and heat of each unit. Allows for units to be
    routed around each other in time and space.'''
    def __init__(self, gc, nav):
        self.gc = gc
        self.nav = nav
        self.__occupations = {} # mapping of turn -> set of occupied
                                # (x, y) tuple locations

    def neighbors(self, node):
        if node.turn >= 1000:
            print('Explored entire search graph! (ideally this never happens)')
            return []
        
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
            return filtered_moves + [dont_move]
        else:
            return [dont_move]

    def __is_clear(self, node):
        '''True iff the given node is not occupied by another unit.'''
        def check_location(location):
            if self.gc.is_occupiable(location):
                return True
            else:
                # could be occupiable later if unit is moving
                unit = self.gc.sense_unit_at_location(location)
                if unit is not None:
                    return unit in self.nav.traveling_units.keys()
                else:
                    # print("This message should happen -- delete it later if it does")
                    return False

        coord = (node.location.x, node.location.y)
        return (check_location(node.location)
                # TODO: check turn and also the turn
                # swap: . 2 1 . ->
                #       . 1 2 . CAN'T HAPPEN
                # move together:
                #       . 2 1 . ->
                #       . . 2 1 CAN HAPPEN - but won't right now

                # TODO: do this smarter
                # Units move towards their occupation each turn.
                # Without knowing order in which units move, we can
                # assume units occupy both the tile they were moved to
                # last turn + the occupation tile this turn.
                and (coord not in self.occupations(node.turn))
                and (coord not in self.occupations((max(node.turn - 1, 0)))))
                    
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
        return abs(x1 - x2) + abs(y1 - y2)

    def success(self, node, goal):
        # Some options here:
        #  1. fail if blocked
        #  2. Choose nearest unoccupied tile to destination (break
        #  ties by closest to unit)
        
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

Route = namedtuple('Route', ['goal', 'route'])

class Navigator:
    # idea: if a circular dependency is detected while scouting, then
    # route those units to each other's spaces if there is one (and
    # then try to reroute) (also still route lazily)

    # flow:
    #  - before moving units, route any unrouted units
    #  - if an unrouted unit is encountered while scouting, route that unit
    
    #     - __find_route -> __scout_blocked ->
    #       a_star_search(loc_graph) ->
    #       loc_graph.continuation/__scout_continuation
    #     - continuation needs: og unit, new unit, deps
    #        - deps passed in as arg
    
    # Overview of process:
    #  - maintain routes of each unit moving towards its destination
    #    and update them as necessary when things change
    #  - move units towards their dests when move_units() is called
    
    def __init__(self, gc):
        self.gc = gc
        self.graph = SearchGraph(gc, self)
        # self.scout_graph = ScoutGraph(gc, self.__scout_continuation)
        # all units bc they are impassable
        self.units = set()
        # units that are moving and their routes
        self.traveling_units = {}
        # units that need to be routed along w their destinations
        self.unrouted_units = {}
        
    def direct_unit(self, unit_id, destination):
        '''Move unit to destination over a number of turns.'''
        self.unrouted_units[unit_id] = destination
        self.units.add(unit_id)

    def free_unit(self, unit_id):
        if unit_id in self.traveling_units.keys():
            del self.traveling_units[unit_id]
        if unit_id in self.unrouted_units.keys():
            del self.unrouted_units[unit_id]

    def move_units(self):
        '''Moves all units towards their destinations.'''
        # units are routed lazily -- that is, their routes are not
        # known until they need to move
        
        # TODO figure out how to
        # properly sequence units for dependencies

        still_unrouted = {} # gross
        
        # route all units that have not yet been routed
        while self.unrouted_units:
            # get one unit and route that one
            id = list(self.unrouted_units.keys())[0]
            # unit = self.gc.unit(id)
            dest = self.unrouted_units[id]
            if self.__find_route(id, dest):
                del self.unrouted_units[id]
                continue
            else:
                print("Can't route", id, "!")
                # Gross
                still_unrouted[id] = self.unrouted_units[id]
                del self.unrouted_units[id]

        self.unrouted_units = still_unrouted
                        
            # that one will encounter and subsequently route other units
            # get another unit
        
        units_to_move = [u for u in self.traveling_units
                         if self.gc.unit(u).is_move_ready()]
        arrived_units = []
        blocked_units = []
        for id, route in self.traveling_units.items():
            unit = self.gc.unit(id)
            if not route:
                print('unit', id, 'has no route!!!')
                continue
            dest = route[-1]
            # if unit.is_move_ready(): # TODO - be more careful here
            move = route.popleft()
            dir = unit.location.map_location().direction_to(move)
            if dir is Direction.Center:
                continue
            elif self.gc.can_move(id, dir):
                print("moving unit", id)
                self.gc.move_robot(id, dir)
                if unit.location.map_location() == dest:
                    print('Unit', id, 'arrived at destination', (dest.x, dest.y))
                    arrived_units.append(id)
            else:
                print("Unit", id, "is blocked! Rerouting next turn...")
                blocked_units.append(id)
        for unit in arrived_units:
            self.free_unit(unit)
        for unit in blocked_units:
            self.free_unit(id)
            self.direct_unit(id, dest)


    # probably only useful for testing
    def still_navigating(self):
        return ((not not self.traveling_units.keys()) or
                (not not self.unrouted_units.keys()))

    def __find_route(self, unit_id, destination, deps = None):
        '''Routes given unit and appropriately updates data
        structures. Returns true if unit was successfully routed,
        false otherwise.'''
        print("Finding route for unit", unit_id)
        if deps is None:
            deps = {}
        unit = self.gc.unit(unit_id)
        start_loc = unit.location.map_location()
        # first try to get there with plain old location search.
        if self.__scout_blocked(unit_id, start_loc, destination, deps):
            print('unit', unit_id, "can't find a route!")
            return False
        start = SearchNode(start_loc, self.gc.round(), unit_id, unit.movement_heat())
        goal = destination
        came_from, end = a_star_search(self.graph, start, goal)
        if end is None:
            return False
        path = reconstruct_path(came_from, start, end)
        path = deque([node.location for node in path])
        self.traveling_units[unit_id] = path
        print('routed unit', unit_id, '\n')
        return True
    
    def __scout_blocked(self, unit_id, start_loc, dest_loc, deps):
        '''Returns true if path is blocked.'''
        # idea: if we encounter one of our own units that is not yet
        # routed, route that unit, then finish routing ourselves
        
        # better idea: if we encounter one of our own units, only
        # route that one if scout search fails. Do this using a data
        # structure to store all potentially blocking units (in order)

        start = LocationNode(start_loc)
        dest = LocationNode(dest_loc)
        # because we passed in scout_continuation to scout_graph,
        # scout_graph will call it when it encounters a unit while
        # scouting

        # this time:
        #  call a continuation that modifies a dependencies object
        #  that we own to append encountered units. Then we process
        #  those encountered units if we fail.
        self.scout_graph = ScoutGraph(self.gc, unit_id, deps,
                                      self.__scout_continuation)
        came_from, end = a_star_search(self.scout_graph, start, dest)
        if end is not None:
            print('successfully scouted...')
            return False
        if end is None:
            print("couldn't find a route for", unit_id, "-- now checking other units")
            print(deps)

            if cyclic(deps):

                raise Exception("circular deps detected; implement me")
            
            for other_id in deps[unit_id]:
                dest = self.unrouted_units[other_id]
                if self.__find_route(other_id, dest, deps):
                    del self.unrouted_units[other_id]
                    return False
                else:
                    print('failed routing', str(other_id) + ';', 'continuing...')
                    continue 
        return True

    def __scout_continuation(self, unit_id, other_id, deps):
        '''Return true if location is occupiable.'''
        if unit_id == other_id:
            return True
        if other_id in self.traveling_units.keys():
            print("found traveling unit", other_id)
            # problem: what if a unit is traveling now, but will be
            # blocking in a bit?
            return True
        elif other_id in self.unrouted_units.keys():
            print('found unrouted unit', other_id)
            # update dependencies
            if other_id not in deps.keys(): # we haven't explored this node yet
                if unit_id in deps.keys():
                    deps[unit_id].append(other_id)
                else:
                    deps[unit_id] = [other_id]

            return False
        elif other_id in self.units:
            print("found stationary unit", unit_id,
                  "-- hopefully this doesn't happen often")
            print(deps)
            return False
        else:
            print('Found unknown unit', other_id)
            return False

    def __scout_continuation_old(self, unit_id, other_id, deps):
        '''Update deps for unit_id, route other_id (and any other units that
        are encountered while routing other_id.'''
        if other_id in self.traveling_units.keys():
            # problem: what if a unit is traveling now, but will be
            # blocking in a bit?
            return True 
        elif other_id in self.unrouted_units.keys():
            # update dependencies, route that unit now
            if unit_id in deps:
                if other_id in deps[unit_id]:
                    raise Exception("CIRCULAR DEPS: fuckin check ur dependencies")
                deps[unit_id].append(other_id)
            else:
                deps[unit_id] = [other_id]
            # check for circular deps:
            if cyclic(deps):
                raise Exception("circular deps detected; implement me")
            dest = self.unrouted_units[unit_id]
            if self.__find_route(other_id, dest, deps):
                del self.unrouted_units[other_id]
                return True
            else:
                raise Exception("???")
        elif other_id in self.units:
            print("hopefully this doesn't happen often")
            return False
        else:
            raise Exception("!!!")
        

    def __make_scout_continuation(self, cands):
        def scout_continuation(unit_id, other_id, deps):
            '''Return true if location is occupiable.'''
            if unit_id == other_id:
                return True
            if other_id in self.traveling_units.keys():
                print("found traveling unit", other_id)
                # problem: what if a unit is traveling now, but will be
                # blocking in a bit?
                return True
            elif other_id in self.unrouted_units.keys():
                print('found unrouted unit', other_id)
                cands.append(other_id)
                return False
            elif other_id in self.units:
                print("hopefully this doesn't happen often")
                return False
            else:
                print('Found unknown unit', other_id)
                return False
        return scout_continuation


### Backup Navigation ######################################
# TODO Idea is to keep track of total movement of units and fall back
# to decentralized control (like bug nav in an availability-first
# order) if it falls below a given threshold. Would prevent failures
# in pathfinding algorithm from screwing us.
