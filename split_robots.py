import battlecode as bc
import random
import sys
import traceback

from task_mgmt import task_mgmt

def split_robots(units, worker_objects, factory_objects, soldier_objects):
    """
    takes in all units from gc.units(), and splits them into groups for sending to controllers

    returns lists of units
    """

    #TODO invert function to check if units have died and pull them,
    # will likely cause some reference errors

    #make list of all_units
    all_objects = worker_objects + factory_objects +soldier_objects
    all_units_last_turn =[]
    for robot in all_objects:
        all_units_last_turn.append(robot.unit)



    #loops through units at start of this turn
    for unit in units:
        #checks if the unit is new, by check if existed last turn
        if unit not in all_units_last_turn:
            #if no, make the object and add it to its object list
            if unit.unit_type is bc.UnitType.Worker:
                new_unit = task_mgmt.Worker(unit)
                worker_objects.append(new_unit)
            if unit.unit_type is bc.UnitType.Factory:
                new_unit = task_mgmt.Worker(unit)
                factory_objects.append(new_unit)
            #TODO add other military units
            if unit.unit_type is bc.UnitType.Ranger:
                new_unit = task_mgmt.Worker(unit)
                soldier_objects.append(new_unit)
    print("all objects", worker_objects,  factory_objects, soldier_objects)
    return worker_objects,  factory_objects, soldier_objects
