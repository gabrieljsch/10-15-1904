from collections import namedtuple

from nav import Navigator
from ..battlecode import Direction

# Mocks
Location = namedtuple('Location', ['x', 'y'])

class Unit:
    def __init__(self, id, location):
        self.id = id
        self.location = location
        self.heat = 0

    def movement_heat(self):
        return self.heat
        
    def is_move_ready(self):
        return self.heat < 10

def loc_to_coord(loc):
    return (loc.x, loc.y)

def coord_to_loc(coord):
    x, y = coord
    return Location(x, y)

### Model of the world #####################################
class World:
    def __init__(self, width, init_string):
        self.units = {}
        self.obstacles = set()
        self.goal = None
        self.width = width
        self.rnd = 0
        self.height = self.__parse_init_string(init_string)

    def __add_obstacle(self, coord):
        self.obstacles.add(coord)

    def __add_goal(self, coord):
        self.goal = coord_to_loc(coord)

    def __add_unit(self, id, coord):
        self.units[id] = Unit(id, coord_to_loc(coord))

    def unit(self, id):
        return self.units[id]
        
    def move_robot(self, id, direction):
        unit = self.units[id]
        x, y = loc_to_coord(unit.location)
        dx, dy = self.__dir_to_delta(dir)
        new_coord = (x + dx, y + dy)
        if self.is_occupiable(new_coord):
            unit.location = coord_to_loc(new_coord)
            unit.heat += 20
        else:
            raise Exception("Robot " + str(id) + " can't move to " +
                            str(new_coord) + "!")
    
    def sense_unit_at_location(self, location):
        matching_unit = [id for id in self.units.keys() if
                         loc_to_coord(self.units[id].location)
                         == (location.x, location.y)]
        if matching_unit:
            return matching_unit[0]
        else:
            return None

    def is_occupiable(self, location):
        coord = (location.x, location.y)
        return (coord in self.obstacles
                or coord in [loc_to_coord(u.location) for u in self.units.values()])

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
            elif char in "G*":
                self.__add_goal(loc)
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

    def __dir_to_delta(dir):
        if dir is Direction.East:
            return (-1, 0)
        elif dir is Direction.North:
            return (0, -1)
        elif dir is Direction.Northeast:
            return (-1, -1)
        elif dir is Direction.Northwest:
            return (1, -1)
        elif dir is Direction.South:
            return (0, 1)
        elif dir is Direction.Southeast:
            return (-1, 1)
        elif dir is Direction.Southwest:
            return (1, 1)
        elif dir is Direction.West:
            return (1, 0)
        elif dir is Direction.Center:
            return (0, 0)
        else:
            print("Direction not recognized!")

    def to_string(self):
        '''Give a printed representation of the world at this point'''
        out = [['.' for i in range(self.width)] for j in range(self.height)]
        # write all data structures to output list:
        for id, unit in self.units.items():
            x,y = loc_to_coord(unit.location)
            out[x][y] = str(id)
        for (x, y) in self.obstacles:
            out[x][y] = '#'
        (x, y) = self.goal
        out[x][y] = '*' # TODO multiple goals

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
. . . . . . .
. 1 . . . * .
. . . . . . .
. . . . . . .
. . . . . . .
"""

ez_world = World(7, easy)
print(ez_world.to_string())
nav = Navigator(ez_world)
nav.direct_unit(1, ez_world.goal)
while nav.still_navigating():
    nav.move_units()
    print(ez_world.to_string())
    ez_world.end_turn()


simple_blocked ="""
. . . # . . .
. . . # . . .
. . . # . . .
. 1 . # . * .
. . . # . . .
. . . # . . .
. . . # . . .
"""

tunnel = """
 . . . . * . . . . . . . 
 . . . # . # . . . . . . 
 . . . # . # . . . . . . 
 . . . # 1 # . . . . . . 
 . . . # 2 # . . . . . . 
 . . . # 3 # . . . . . . 
 . . . # . # . . . . . . 
 . . . # . # . . . . . . 
 . . . # . # . . . . . . 
 . . . # . # . . . . . . 
 . . . . . . . . . . . . 
"""

bad_tunnel = """
....*.......
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


            

