
import battlecode as bc
import random
import sys
import traceback

from move_random_after_block import move_random_after_block


def move_directly(gc, unit,location_to_go):
    """
    sends a unit directly to a map location
    inputs are gc, unit as a unit, and a map location

    """

    #get unit map location
    map_loc = unit.location.map_location()
    #get direction to objective
    direction_to_go = map_loc.direction_to(location_to_go)
    directions = list(bc.Direction)

    #check cooldown
    if unit.movement_heat() < 10:
    #move robot
        try:
            if gc.can_move(unit.id,direction_to_go) == True:
                gc.move_robot(unit.id, direction_to_go)

            else:
                try:
                    move_random_after_block(gc, unit)

                except:
                    traceback.print_exc()

        except:
            traceback.print_exc()
