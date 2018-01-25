import battlecode as bc
import random
import sys
import traceback

from find_safe_landing_loc import find_safe_landing_loc

def rocket_supervisor(gc,rockets, worker_objects):



    #for each rockets
    for rocket in rockets:
        for worker in worker_objects:
            if gc.can_load(rocket.id,worker.unit.id):
                gc.load(rocket.id,worker.unit.id)
                # print("tried to yank him")
                # worker_objects.remove(worker)

        if len(rocket.structure_garrison()) > 0:
            destination = find_safe_landing_loc(gc)
            if gc.can_launch_rocket(rocket.id, destination) == True:
                gc.launch_rocket(rocket.id, destination)
    return worker_objects
    #try to load all of the units we can
