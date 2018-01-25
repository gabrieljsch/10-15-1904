import battlecode as bc
import random
import sys
import traceback

def find_safe_landing_loc(gc):

    mars = bc.Planet.Mars
    mars_map = gc.starting_map(mars)
    height, width = gc.starting_map(mars).height, gc.starting_map(mars).width


    done = 0
    while done != 1:
        location_x = random.randrange(width)
        location_y = random.randrange(height)
        map_location = bc.MapLocation(mars,location_x,location_y)
        if mars_map.is_passable_terrain_at(map_location):
            return map_location
