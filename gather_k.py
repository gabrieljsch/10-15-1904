
import battlecode as bc
import random
import sys
import traceback

def gather_k(gc, worker):
    """
    tells unit to gather karbonite, then move one square right
    and try again. Inputs are gc and worker (a unit)
    """

    try:
        #if it can harvest do
        if gc.can_harvest(worker.id, bc.Direction.East)==True:
            gc.harvest(worker.id, bc.Direction.East)
        else:
            try:
                #if it cant, can it move right. If so move
                if gc.can_move(worker.id, bc.Direction.East):
                    gc.move_robot(worker.id, bc.Direction.East)
            except:
                traceback.print_exc()
    except:
        traceback.print_exc()
