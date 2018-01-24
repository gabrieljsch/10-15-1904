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
    all_objects = worker_objects + factory_objects + soldier_objects
    all_units_last_turn = []
    for robot in all_objects:
        all_units_last_turn.append(robot.unit.id)


    #id_list
    id_list = []
    for unit in units:
        id_list.append(unit.id)

    #creates new lists
    new_worker_objects =[]
    new_factory_objects= []
    new_soldier_objects = []
    unbuilt_structures =[]

    for i in range(len(all_objects)):

        if all_objects[i].unit.id in id_list:
            #resets the units of all old objects
            robot = all_objects[i]
            new_unit = gc.unit(all_objects[i].unit.id)
            old_task = all_objects[i].task
            new_object = task_mgmt.Worker(new_unit)
            new_object.assign(old_task)
            #spreads them
            if robot in worker_objects:
                new_worker_objects.append(new_object)

            if robot in factory_objects:
                new_factory_objects.append(new_object)

            if robot in soldier_objects:
                new_soldier_objects.append(new_object)



    #loops through units at start of this turn
    for unit in units:
        #check if unbuilt factory (or rocket?)
        if unit.unit_type == bc.UnitType.Factory and unit.structure_is_built() == False:
            unbuilt_structures.append(unit)
            continue
        #checks if the unit is new, by check if existed last turn
        if unit.id not in all_units_last_turn:
            #if no, make the object and add it to its object list
            if unit.unit_type is bc.UnitType.Worker:
                new_unit = task_mgmt.Worker(unit)
                new_worker_objects.append(new_unit)
            if unit.unit_type is bc.UnitType.Factory:
                if unit.structure_is_built() == True:
                    new_unit = task_mgmt.Worker(unit)
                    new_factory_objects.append(new_unit)
            #TODO add other military units
            if unit.unit_type is bc.UnitType.Ranger:
                new_unit = task_mgmt.Worker(unit)
                new_soldier_objects.append(new_unit)



    return new_worker_objects, new_factory_objects, new_soldier_objects, unbuilt_structures
