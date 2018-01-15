
import battlecode as bc
import random
import sys
import traceback

from move_random_after_block import move_random_after_block
def gather_k(gc, worker):
    """
    tells unit to gather karbonite, then move one square right
    and try again. Inputs are gc and worker (a unit)
    """
    directions = list(bc.Direction)

    try:
        #if it can harvest do
        for direction in directions:
            if gc.can_harvest(worker.id, direction)==True:
                gc.harvest(worker.id, direction)
        try:
            #if it cant, can it move right. If so move
            move_random_after_block(gc, worker)
        except:
            traceback.print_exc()
    except:
        traceback.print_exc()
