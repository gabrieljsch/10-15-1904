import battlecode as bc
import random
import sys
import traceback

def make_location(gc,x,y):
    """
    makes a map location on earth
    """
    
    map_location = bc.MapLocation(bc.Planet.Earth,x,y)
    return map_location
