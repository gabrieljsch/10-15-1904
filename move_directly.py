
import battlecode as bc
import random
import sys
import traceback


def move_directly(gc, unit,location_to_go):
    unit_location = unit.location
    map_loc = unit_location.map_location()
    direction_to_go = map_loc.direction_to(location_to_go)
    print("direction to go", direction_to_go)
    print("Robot at", map_loc)

    if unit.movement_heat() < 10:
    #move robot
        try:
            print("unit id", unit.id)
            print(gc.can_move(unit.id,direction_to_go))
            gc.move_robot(unit.id, direction_to_go)
            print("print(did it move?", unit.location)
        except:
            print("actual move failed")
            traceback.print_exc()
            pass
