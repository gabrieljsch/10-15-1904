import battlecode as bc
import random
import sys
import traceback

directions = [bc.Direction.North, bc.Direction.Northeast, bc.Direction.East, bc.Direction.Southeast, bc.Direction.South, bc.Direction.Southwest, bc.Direction.West, bc.Direction.Northwest]

def main_mars(gc):
    """
    is the bot that runs all things mars, called each turn

    """
    my_units = gc.units()

    #get rocket to unpack
    if len(my_units)>0:
        print("in mars loop")
        for unit in my_units:
            if unit.unit_type == bc.UnitType.Rocket:
                print("on rocket")
                if len(unit.structure_garrison()) != 0:
                    for direction in directions:
                        if gc.can_unload(unit.id, direction):
                            gc.unload(unit.id, direction)
