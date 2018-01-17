
import battlecode as bc
import random
import sys
import traceback

from move_directly import move_directly
from move_random_after_block import move_random_after_block
from soldier_move import soldier_move

directions = list(bc.Direction)


def military_supervisor(gc, soldier_objects, factory_objects, enemy_dir, home_loc, attack_dir):
    """
    supervises military units. In this case,builds 7 rangers,lines them
    diagonally in front of the base, then charges accross the map and attacks

    imputs are gc, soldier list, and factory list
    """

    fac_location = factory_objects[0].unit.location.map_location()
    release_direction = enemy_dir



    if gc.team() is bc.Team.Red:
        oppo_team = bc.Team.Blue
    else:
        oppo_team = bc.Team.Red

    #sets charge switch
    switch = 1

    #if building up
    try:
        #if we have any soldiers
        if len(soldier_objects) > 0:
            #enumerate soldiers
            for i in range(len(soldier_objects)):
                #if soldier in garrison
                if soldier_objects[i].unit.location.is_in_garrison() ==True:
                    garr_id = soldier_objects[i].unit.location.structure()
                    #try to pull him out
                    if gc.can_unload(garr_id, release_direction)==True:
                        gc.unload(garr_id, release_direction)
                    else:
                        for i in directions:
                            if gc.can_unload(garr_id, i)==True:
                                gc.unload(garr_id, i)
    except:
        traceback.print_exc()

    # if we are charging
    try:
        if switch == 1:
            #for each soldier
            full_unit_seen_list = []
            for soldier in soldier_objects:
                soldier = soldier.unit
                #check if we see any enemies
                try:
                    print("look around",soldier.location.is_in_garrison(), soldier.location, soldier.id)

                    if soldier.location.is_in_garrison() != True:
                        units_near = gc.sense_nearby_units_by_team(soldier.location.map_location(), soldier.attack_range(), oppo_team)
                        print("units near", units_near)
                    else:
                        units_near = []
                except:
                    units_near = []
                    traceback.print_exc()
                #if we do
                if len(units_near) != 0:
                    print("try to get em!")
                    #try to attack then do
                    if gc.can_attack(soldier.id, units_near[0].id) == True:
                        if soldier.attack_heat() < 10:
                            gc.attack(soldier.id, units_near[0].id)

                    for unit in units_near:
                        if unit not in full_unit_seen_list:
                            full_unit_seen_list.append(unit)
                #else continue charge
                else:
                    #sets var for random vs move toward
                    attack_dir = soldier_move(gc, soldier, full_unit_seen_list, enemy_dir, home_loc, attack_dir)

    except:
        traceback.print_exc()

    return soldier_objects
