
import battlecode as bc
import random
import sys
import traceback

from move_directly import move_directly

def military_supervisor(gc, soldiers, factories):
    """
    supervises military units. In this case,builds 7 rangers,lines them
    diagonally in front of the base, then charges accross the map and attacks

    imputs are gc, soldier list, and factory list
    """


    if gc.team() is bc.Team.Red:
        x = 10
        y = 4
        release_direction = bc.Direction.North
        charge_direction = bc.Direction.Northeast
        oppo_team = bc.Team.Blue

    else:
        x = 16
        y = 13
        release_direction = bc.Direction.South
        charge_direction = bc.Direction.Southwest
        oppo_team = bc.Team.Red

    #sets charge switch
    if gc.round() <= 120:
        switch = 0
    else:
        switch = 1

    #if building up
    try:
        if switch == 0:
            #if we have any soldiers
            if len(soldiers) > 1:
                #enumerate soldiers
                for i in range(len(soldiers)):
                    #if soldier in garrison
                    if soldiers[i].location.is_in_garrison() ==True:
                        #try to pull him out
                        if gc.can_unload(factories[0].id, release_direction)==True:
                            gc.unload(factories[0].id, release_direction)
                    # if already out
                    if soldiers[i].location.is_in_garrison() ==False:
                        try:
                            #try to move him to the diagnol
                            move_directly(gc, soldiers[i], bc.MapLocation(bc.Planet.Earth, x-i, y+i))

                        except:
                            traceback.print_exc()
    except:
        traceback.print_exc()

    # if we are charging
    try:
        if switch == 1:
            #for each soldier
            for soldier in soldiers:
                #check if we see any enemies
                units_near = gc.sense_nearby_units_by_team(soldier.location.map_location(), soldier.attack_range(), oppo_team)
                #if we do
                if len(units_near) != 0:
                    #try to attack then do
                    if gc.can_attack(soldier.id, units_near[0].id) == True:
                        if soldier.attack_heat() < 10:
                            gc.attack(soldier.id, units_near[0].id)
                #else continue charge
                else:
                    if gc.can_move(soldier.id, charge_direction) == True:
                        if soldier.movement_heat() < 10:
                            gc.move_robot(soldier.id, charge_direction)

    except:
        traceback.print_exc()
