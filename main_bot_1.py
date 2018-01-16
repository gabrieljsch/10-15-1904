import battlecode as bc
import random
import sys
import os
import traceback

from move_directly import move_directly
from make_factory_at import make_factory_at
from split_robots import split_robots
from worker_ai import worker_ai
from factory_supervisor import factory_supervisor
from gather_k import gather_k
from military_supervisor import military_supervisor


from task_mgmt import task_mgmt
from tasks import harvest

gc = bc.GameController()


# A GameController is the main type that you talk to the game with.
# Its constructor will connect to a running game.
# gc = bc.GameController()
directions = list(bc.Direction)

# random.seed(6)

# need_factory = 1
#Running bot
while True:

    #only run earth and red team
    if gc.planet() is bc.Planet.Earth:

        if gc.round() % 50 == 0:
            print("Round is:", gc.round())

        #set home location
        if gc.team() is bc.Team.Red:
            home_loc = bc.MapLocation(bc.Planet.Earth, 1,1)
        else:
            home_loc = bc.MapLocation(bc.Planet.Earth, 19,19)
        #split units
        try:
            workers, soldiers, factories = split_robots(gc.my_units())
        except:
            traceback.print_exc()

        if gc.round() == 1:
            worker_objects = set([task_mgmt.Worker(worker) for worker in workers])
            for worker_o in worker_objects:
                harvest_task = harvest.Harvest_then_build(worker_o)
                worker_o.assign(harvest_task)
                print('assigned',worker_o.unit.id)

        for worker_object in worker_objects:
                

            if worker_object.task is not None:
                worker_object.work()

        #set initial values
        # try:
        #     if need_factory ==1:
        #         need_factory = worker_ai(gc, workers, factories, need_factory, home_loc)
        # except:
        #     traceback.print_exc()

        # try:
        #     factory_supervisor(gc,factories, soldiers)
        # except:
        #     traceback.print_exc()

        # try:
        #     if need_factory == 0:
        #         gather_k(gc, workers[0])
        # except:
        #     traceback.print_exc()

        # try:
        #     military_supervisor(gc, soldiers, factories)
        # except:
        #     traceback.print_exc()



    # send the actions we've performed, and wait for our next turn.
    gc.next_turn()

    # these lines are not strictly necessary, but it helps make the logs make more sense.
    # it forces everything we've written this turn to be written to the manager.
    sys.stdout.flush()
    sys.stderr.flush()
