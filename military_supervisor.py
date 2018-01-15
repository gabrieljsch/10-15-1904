
import battlecode as bc
import random
import sys
import traceback

from move_directly import move_directly
from move_random_after_block import move_random_after_block

directions = list(bc.Direction)

def military_supervisor(gc, soldiers, factories, enemy_loc, home_loc):
    """
    supervises military units. In this case,builds 7 rangers,lines them
    diagonally in front of the base, then charges accross the map and attacks

    imputs are gc, soldier list, and factory list
    """

    if len(factories) == 0:
        release_direction = bc.Direction.North
    else:
        fac_location = factories[0].location.map_location()
        release_direction = home_loc.direction_to(enemy_loc)

    barrier = .8

    if gc.team() is bc.Team.Red:
        oppo_team = bc.Team.Blue

    else:
        oppo_team = bc.Team.Red

    #sets charge switch
    if gc.round() <= 10:
        switch = 0
    else:
        switch = 1


    #if building up
    try:
        #if we have any soldiers
        if len(soldiers) > 0:
            #enumerate soldiers
            for i in range(len(soldiers)):
                #if soldier in garrison
                if soldiers[i].location.is_in_garrison() ==True:
                    garr_id = soldiers[i].location.structure()
                    #try to pull him out
                    if gc.can_unload(garr_id, release_direction)==True:
                        print("unload", garr_id, gc.round())
                        gc.unload(garr_id, release_direction)
                    else:
                        for i in directions:
                            if gc.can_unload(garr_id, i)==True:
                                print("unload", garr_id, gc.round())
                                gc.unload(garr_id, i)
    except:
        traceback.print_exc()

    # if we are charging
    try:
        if switch == 1:
            #for each soldier
            for soldier in soldiers:
                #check if we see any enemies

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
                #else continue charge
                else:
                    #sets var for random vs move toward
                    if gc.is_move_ready(soldier.id) ==True:
                        which_way = random.random()
                        if which_way < barrier:
                            if gc.can_move(soldier.id, release_direction)==True:
                                gc.move_robot(soldier.id, release_direction)

                            else:
                                move_random_after_block(gc, soldier)

                        if which_way >= 1.0-barrier:
                            try:
                                move_random_after_block(gc,soldier)
                            except:
                                traceback.print_exc()

    except:
        traceback.print_exc()
