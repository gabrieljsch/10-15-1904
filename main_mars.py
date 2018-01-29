import battlecode as bc
import random
import sys
import traceback

directions = [bc.Direction.North, bc.Direction.Northeast, bc.Direction.East, bc.Direction.Southeast, bc.Direction.South, bc.Direction.Southwest, bc.Direction.West, bc.Direction.Northwest]

def main_mars(gc):
    """
    is the bot that runs all things mars, called each turn

    """
    if gc.team() is bc.Team.Red:
        oppo_team = bc.Team.Blue
    else:
        oppo_team = bc.Team.Red

    my_units = gc.units()
    my_workers = []
    my_soldiers = []
    #split units
    for unit in my_units:
        if unit.unit_type == bc.UnitType.Worker:
            my_workers.append(unit)
        if unit.unit_type == bc.UnitType.Ranger:
            my_soldiers.append(unit)

    #get rocket to unpack
    if len(my_units)>0:
        for unit in my_units:

            #if it is a rocket, try unloading
            if unit.unit_type == bc.UnitType.Rocket:
                if len(unit.structure_garrison()) != 0:
                    for direction in directions:
                        if gc.can_unload(unit.id, direction):
                            gc.unload(unit.id, direction)


            #worker formula lol
            workers_needed = ((gc.round() - 100)**.8)*.4 -10
            if gc.round() > 750:
                workers_needed = 1000
            #If worker and we need to replicate, try replicating?
            if len(my_units) < workers_needed:
                if unit.unit_type == bc.UnitType.Worker:
                    for direction in directions:
                        if gc.can_replicate(unit.id, direction) == True:
                            gc.replicate(unit.id, direction)
            #if it's a worker, try gathering, else move randomly?
            if unit.unit_type == bc.UnitType.Worker:
                for direction in directions:
                    if gc.can_harvest(unit.id, direction) == True:
                        gc.harvest(unit.id, direction)
                        break
                #move loops
                runner = 0
                while runner < 8:
                    direction = random.choice(directions)
                    runner +=1
                    if gc.can_move(unit.id, direction) == True:
                        if gc.is_move_ready(unit.id) == True:
                            gc.move_robot(unit.id, direction)
                            break

            #mars combat attempt
            if unit.unit_type == bc.UnitType.Ranger:
                soldier = unit
                try:
                    if soldier.location.is_in_garrison() != True:
                        units_near = gc.sense_nearby_units_by_team(soldier.location.map_location(), soldier.attack_range(), oppo_team)
                    else:
                        units_near = []
                except:
                    units_near = []
                    traceback.print_exc()
                #if we do
                if len(units_near) != 0:
                    #try to attack then do
                    if gc.can_attack(soldier.id, units_near[0].id) == True:
                        if soldier.attack_heat() < 10:
                            gc.attack(soldier.id, units_near[0].id)
                else:
                    #move loops
                    runner = 0
                    while runner < 8:
                        direction = random.choice(directions)
                        runner +=1
                        if gc.can_move(soldier.id, direction) == True:
                            if gc.is_move_ready(soldier.id) == True:
                                gc.move_robot(soldier.id, direction)
                                break
