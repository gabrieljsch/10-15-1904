import battlecode as bc
import random
import sys
import traceback



def set_enemy_dir(gc, home_loc):

    #get map_dimesions

    height, width = gc.starting_map(bc.Planet.Earth).height, gc.starting_map(bc.Planet.Earth).width
    #set corners
    ul_corner, ur_corner, bl_corner, br_corner = bc.MapLocation(bc.Planet.Earth, 1,height), bc.MapLocation(bc.Planet.Earth, width, height), bc.MapLocation(bc.Planet.Earth, 1, 1), bc.MapLocation(bc.Planet.Earth,width ,1)

    best_corner = ul_corner
    for corner in [ul_corner, ur_corner, bl_corner, br_corner]:
        if home_loc.distance_squared_to(best_corner) > home_loc.distance_squared_to(corner):
            best_corner = corner
    if best_corner == ul_corner:
        enemy_corner = br_corner
    elif best_corner == ur_corner:
        enemy_corner = bl_corner
    elif best_corner == bl_corner:
        enemy_corner = ur_corner
    elif best_corner == br_corner:
        enemy_corner = ul_corner

    enemy_dir = home_loc.direction_to(enemy_corner)
    return enemy_dir
