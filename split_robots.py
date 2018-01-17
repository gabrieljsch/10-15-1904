import battlecode as bc
import random
import sys
import traceback

from task_mgmt import task_mgmt

def split_robots(units, worker_objects, factory_objects, soldier_objects, gc):
    """
    takes in all units from gc.units(), and splits them into groups for sending to controllers

    returns lists of units
    """

    #TODO invert function to check if units have died and pull them,
    # will likely cause some reference errors

    #make list of all_units
    all_objects = worker_objects + factory_objects +soldier_objects
    all_units_last_turn = []
    for robot in all_objects:
        all_units_last_turn.append(robot.unit.id)


    #id_list
    id_list = []
    for unit in units:
        id_list.append(unit.id)

    for i in range(len(all_objects)):
        #if an old unit is not in units now
        if all_objects[i].unit.id not in id_list:
            robot = all_objects[i]
            if robot in worker_objects:
                worker_objects.remove(robot)
                print("removed", robot.unit)
                print("all units last turn", all_units_last_turn)
                print("my units", units)
            if robot in factory_objects:
                factory_objects.remove(robot)
                print("removed", robot.unit)
                print("all units last turn", all_units_last_turn)
                print("my units", units)
            if robot in soldier_objects:
                soldier_objects.remove(robot)
                print("removed", robot)
                print("all units last turn", all_units_last_turn)
                print("my units", units)








    #loops through units at start of this turn
    for unit in units:
        #checks if the unit is new, by check if existed last turn
        if unit.id not in all_units_last_turn:
            #if no, make the object and add it to its object list
            if unit.unit_type is bc.UnitType.Worker:
                new_unit = task_mgmt.Worker(unit)
                worker_objects.append(new_unit)
            if unit.unit_type is bc.UnitType.Factory:
                if unit.structure_is_built() == True:
                    new_unit = task_mgmt.Worker(unit)
                    factory_objects.append(new_unit)
            #TODO add other military units
            if unit.unit_type is bc.UnitType.Ranger:
                new_unit = task_mgmt.Worker(unit)
                soldier_objects.append(new_unit)
                print("add solider", new_unit)

    return worker_objects, factory_objects, soldier_objects
