
import battlecode as bc
import random
import sys
import traceback


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
                    counter = 0
                    new_dir = random.choice(bc.Direction)
                    while gc.can_move(unit.id, new_dir) == False:
                        new_dir = random.choice(bc.Direction)
                        counter +=1
                        if counter >8:
                            print("cant move")
                    if gc.can_move(unit.id,new_dir) == True:
                        gc.move_robot(unit.id, new_dir)
                except:
                    traceback.print_exc()

        except:
            traceback.print_exc()
