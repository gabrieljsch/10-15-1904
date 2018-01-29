from collections import namedtuple

from nav import Navigator
from battlecode import Direction, Location

directions = [Direction.East,
              Direction.North,
              Direction.Northeast,
              Direction.Northwest,
              Direction.South,
              Direction.Southeast,
              Direction.Southwest,
              Direction.West,
              Direction.Center]

alpha = "abcdefghijklmnopqrstuvwxyz"

def dir_to_delta(dir):
    if dir is Direction.East:
        return (0, 1)
    elif dir is Direction.North:
        return (-1, 0)
    elif dir is Direction.Northeast:
        return (-1, 1)
    elif dir is Direction.Northwest:
        return (-1, -1)
    elif dir is Direction.South:
        return (1, 0)
    elif dir is Direction.Southeast:
        return (1, 1)
    elif dir is Direction.Southwest:
        return (1, -1)
    elif dir is Direction.West:
        return (0, -1)
    elif dir is Direction.Center:
        return (0, 0)
    else:
        print("ERROR Direction not recognized:", dir)

# Mocks
MapLocationBase = namedtuple('MapLocationBase', ['x', 'y'])
class MapLocation(MapLocationBase):
    def add(self, d):
        dx, dy = dir_to_delta(d)
        return MapLocation(self.x + dx, self.y + dy)

    def distance_squared_to(self, other):
        x1, y1 = self.x, self.y
        x2, y2 = other.x, other.y
        return (x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1)
    
    def direction_to(self, other):
        cands = [(self.add(d), d) for d in directions]
        # print([c[0].distance_squared_to(other) for c in cands])
        return min(cands, key = lambda c: c[0].distance_squared_to(other))[1]

class Location:
    def __init__(self, x, y):
        self.mloc = MapLocation(x, y)

    def map_location(self):
        return self.mloc

class Unit:
    def __init__(self, id, location):
        self.id = id
        self.location = location
        self.heat = 0

    def movement_cooldown(self):
        return 20
        
    def movement_heat(self):
        return self.heat
        
    def is_move_ready(self):
        return self.heat < 10

def loc_to_coord(loc):
    return (loc.x, loc.y)

def coord_to_loc(coord):
    x, y = coord
    return MapLocation(x, y)

### Model of the world #####################################
class World:
    def __init__(self, width, init_string):
        self.units = {}
        self.obstacles = set()
        self.goals = {}
        self.width = width
        self.rnd = 0
        self.height = self.__parse_init_string(init_string)

    def __add_obstacle(self, coord):
        self.obstacles.add(coord)

    def __add_goal(self, unit_id, coord):
        self.goals[unit_id] = coord
        # TODO multiple goals
        # self.goal = coord_to_loc(coord)

    def __add_unit(self, id, coord):
        x, y = coord
        self.units[id] = Unit(id, Location(x, y))

    def unit(self, id):
        return self.units[id]
        
    def move_robot(self, id, dir):
        unit = self.units[id]
        if not unit.is_move_ready():
            Exception("Unit " + str(id) + " is not move ready!")
        if dir is Direction.Center:
            print("Probably don't move Direction.center")
            return
        old_location = unit.location.map_location()
        new_location = old_location.add(dir)
        if self.is_occupiable(new_location):
            unit.location.mloc = new_location
            unit.heat += unit.movement_cooldown()
        else:
            raise Exception("Robot " + str(id) + " can't move to " +
                            str(new_location) + "!")
    
    def sense_unit_at_location(self, location):
        matching_unit = [id for id in self.units.keys() if
                         loc_to_coord(self.units[id].location.map_location())
                         == (location.x, location.y)]
        if matching_unit:
            return matching_unit[0]
        else:
            return None

    def is_occupiable(self, location):
        coord = (location.x, location.y)
        return (location.x >= 0 and location.x < self.height and
                location.y >= 0 and location.y < self.width and
                coord not in self.obstacles and
                coord not in [loc_to_coord(u.location.map_location())
                              for u in self.units.values()])

    def can_move(self, id, dir):
        if dir is Direction.Center:
            return True
        unit = self.unit(id)
        return self.is_occupiable(unit.location.map_location().add(dir))

    def end_turn(self):
        self.rnd += 1
        for unit in self.units.values():
            unit.heat -= 10
    
    def round(self):
        return self.rnd

    def __parse_init_string(self, s):
        s = "".join(s.split())
        def do_side_effect(char, loc):
            if char.isdigit(): # it's a unit
                self.__add_unit(int(char), loc)
            elif char in "#|-+": # wall
                self.__add_obstacle(loc)
            elif char in alpha:
                i = alpha.index(char)
                self.__add_goal(i, loc)
            else:
                pass

        if not len(s) % self.width == 0:
            raise Exception("Input string is not multiple of width! ("
                            + str(len(s)) + ", "
                            + str(self.width) + ")")

        height = len(s) // self.width
        
        for (i, char) in enumerate(s):
            loc = (i // self.width, i % self.width)
            do_side_effect(char, loc)

        return height

    def to_string(self):
        '''Give a printed representation of the world at this point'''
        out = [['.' for i in range(self.width)] for j in range(self.height)]
        # write all data structures to output list:
        for x, y in self.obstacles:
            out[x][y] = '#'
        for id, goal in self.goals.items():
            x, y = goal
            out[x][y] = alpha[id]
            # out[x][y] = '*' # TODO multiple goals
        for id, unit in self.units.items():
            x, y = loc_to_coord(unit.location.map_location())
            out[x][y] = str(id)


        # put spaces so it's pretty:
        add_space = lambda c: (c, ' ')
        flatten = lambda l: [item for sublist in l for item in sublist]
        nice_out = "\n".join(["".join(flatten([add_space(e) for e in row])).strip()
                            for row in out]) + "\n"
        return nice_out

### Tests ##################################################

easy = """
. . . . . . .
. . . . . . .
. . . # . . .
. 0 . # . a .
. . . # . . .
. . . . . . .
. . . . . . .
"""

harder = """
. . . . # . .
. . # . # . .
. . # . # . .
. 0 # . # a .
. . # . # . .
. . # . # . .
. . # . . . .
"""

simple_blocked ="""
. . . # . . .
. . . # . . .
. . . # . . .
. 0 . # . a .
. . . # . . .
. . . # . . .
. . . # . . .
"""

tunnel = """
. . . b a c . . . . . . 
. . . # # # . . . . . . 
. . . # . # . . . . . . 
. . . # 0 # . . . . . . 
. . . # 1 # . . . . . . 
. . . # 2 # . . . . . . 
. . . # . # . . . . . . 
. . . # . # . . . . . . 
. . . # . # . . . . . . 
. . . # . # . . . . . . 
. . . . . . . . . . . . 
"""

hard = """
. . . . . . . . . . . . 
. . . 1 # # . . . . . . 
. . b # . # . . . . . . 
. . c # 0 # . . . . . . 
. . a # 2 # . . . . . . 
. . . # . # . . . . . . 
. . . # . # . . . . . . 
. . . # . # . . . . . . 
. . . # . # . . . . . . 
. . . # # # . . . . . . 
. . . . . . . . . . . . 
"""

hard2 = """
. . . . . . . . . . . . 
. . a b # # # . . . . . 
. . c # 1 . # . . . . .
. . . # 0 . # . . . . .
. . . # 2 . # . . . . .
. . . # . . # . . . . .
. . . # . . # . . . . .
. . . # . . # . . . . .
. . . # . . # . . . . .
. . . # # # # . . . . . 
. . . . . . . . . . . . 
"""

circular_deps = """
. . . . . . . .
. # # # # # # .
. # . 0 c . # .
. # . # # 1 # .
. # . # # a # .
. # . b 2 . # .
. # # # # # # .
. . . . . . . .
"""

# ez_world = World(7, harder)
# world = World(12, hard2)
# print(world.to_string())
# nav = Navigator(world)
# units = [0, 1, 2]
# for u in units:
#     nav.direct_unit(u, coord_to_loc(world.goals[u]))
# while nav.still_navigating():
#     nav.move_units()
#     print(world.to_string())
#     world.end_turn()
#     input()

world = World(12, hard)
print(world.to_string())
nav = Navigator(world)
units = [0, 1, 2]
for u in units:
    nav.direct_unit(u, coord_to_loc(world.goals[u]))
while nav.still_navigating():
    nav.move_units()
    print(world.to_string())
    world.end_turn()
    input()


bad_tunnel = """
...abc.....
...#.#......
...#.#......
...#3#......
...#2#......
...#1#......
...#.#......
...#.#......
...#.#......
...#.#......
............
"""
