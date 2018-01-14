import battlecode as bc
import random
import sys
import traceback


def split_robots(units):
    """
    takes in all units from gc.units(), and splits them into groups for sending to controllers

    returns lists of units
    """

    #declare lists of units
    workers = []
    soldiers = []
    factories = []

    #does not include fighting units yet
    
    try:
        if len(units) != 0:
            for i in range(len(units)):
                unit = units[i]
                if unit.unit_type is bc.UnitType.Worker:
                    workers.append(unit)
                if unit.unit_type is bc.UnitType.Factory:
                    factories.append(unit)
                if unit.unit_type is bc.UnitType.Ranger:
                    soldiers.append(unit)

    except:
        traceback.print_exc()




    return workers, soldiers, factories
