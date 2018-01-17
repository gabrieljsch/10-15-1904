
import battlecode as bc
import random
import sys
import traceback

from move_random_after_block import move_random_after_block
from move_directly import move_directly
def gather_k(gc, worker, started_with_karbonite, home_loc):
    """
    tells unit to gather karbonite, then move one square right
    and try again. Inputs are gc and worker (a unit)
    """
    directions = list(bc.Direction)

    if len(started_with_karbonite) != 0:
        try:
            first_go = started_with_karbonite[0]
            for location in started_with_karbonite:
                worker_loc = worker.location.map_location()
                if worker_loc.distance_squared_to(location) < worker_loc.distance_squared_to(first_go):
                    first_go = location
                #also remove blank squares?
                if gc.can_sense_location(location) == True:
                    if gc.karbonite_at(location) < 1:
                        started_with_karbonite.remove(location)

            #if it can harvest do
            if gc.can_harvest(worker.id, bc.Direction.Center)==True:
                gc.harvest(worker.id, bc.Direction.Center)
            else:
                for direction in directions:
                    if gc.can_harvest(worker.id, direction)==True:
                        gc.harvest(worker.id, direction)
                        break
            try:
                #if it cant, can it move right. If so move
                move_directly(gc, worker, first_go)
                # move_random_after_block(gc, worker)
            except:
                traceback.print_exc()
        except:
            traceback.print_exc()
