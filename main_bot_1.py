import battlecode as bc
import random
import sys
import traceback

from move_directly import move_directly
from make_factory_at import Make_factory_at
from split_robots import split_robots
from worker_ai import worker_ai
from factory_supervisor import Factory_supervisor
from gather_k import Gather_k
from military_supervisor import military_supervisor
from set_enemy_dir import set_enemy_dir
from find_home_loc import find_home_loc
from on_turn_one import on_turn_one
from find_fac_loc import find_fac_loc

# Template for importing files
from task_mgmt import task_mgmt
from tasks import harvest

print("running")
gc = bc.GameController()


# A GameController is the main type that you talk to the game with.
# Its constructor will connect to a running game.
# gc = bc.GameController()
directions = list(bc.Direction)

# random.seed(6)


#make worker object lists
worker_objects = []
factory_objects = []
soldier_objects = []



##All info for kyle's helper functions
if gc.planet() is bc.Planet.Earth:
    started_with_karbonite, attack_dir, breaker, workers_needed, factories_needed, enemy_dir, home_loc = on_turn_one(gc)


#Running bot
while True:

    #only run earth
    if gc.planet() is bc.Planet.Earth:


        # split units into respective groups
        worker_objects, factory_objects, soldier_objects  = split_robots(gc.my_units(), worker_objects, factory_objects, soldier_objects, gc)
        all_objects = worker_objects+ factory_objects+ soldier_objects

        #worker controls

        #if we dont have enough workers but have 1
        if len(worker_objects) != 0 and len(worker_objects)<= workers_needed:
            for worker_object in worker_objects:
                worker = worker_object.unit.id
                print(worker)
                replicated = 0
                while replicated < 8:
                    direction = directions[replicated]
                    if gc.can_replicate(worker, direction):
                        gc.replicate(worker, direction)
                        replicated = 10
                    else:
                        replicated +=1



        #if we have enough workers and need factories
        if len(worker_objects) > workers_needed:
            if len(factory_objects) < factories_needed:
                builder = worker_objects[0]
                if builder.task is None:
                    print('assigned:',builder.unit.id)
                    builder.assign(Make_factory_at(gc, builder, find_fac_loc(gc, home_loc), enemy_dir))
            else:
                if builder.task is None:
                    print('assigned to gather builder:',builder.unit.id)
                    builder.assign(Gather_k(gc, builder, started_with_karbonite, home_loc))

        if gc.round() == 10:
            for worker_o in worker_objects:
                if worker_o.task is None and worker_o != worker_objects[0]:
                    print('assigned to gather other:',worker_o.unit.id)
                    worker_o.assign(Gather_k(gc, worker_o, started_with_karbonite, home_loc))

        #factory_controls
        if len(factory_objects) !=0:
            for factory in factory_objects:
                if factory.task is None:
                    factory.assign(Factory_supervisor(gc, factory, soldier_objects, worker_objects))


        #soldier controllers
        if len(soldier_objects) > 0:
            soldier_objects = military_supervisor(gc, soldier_objects, factory_objects, enemy_dir, home_loc, attack_dir)


        #check printng loop
        if gc.round() % 50 == 0:
            print("Round is:", gc.round())
            print("worker objects", worker_objects)
            print("starting carb", started_with_karbonite)

        #main worker loop
        for worker_object in all_objects:
            if worker_object.task is not None:
                worker_object.work()


    # send the actions we've performed, and wait for our next turn.
    gc.next_turn()

    # these lines are not strictly necessary, but it helps make the logs make more sense.
    # it forces everything we've written this turn to be written to the manager.
    sys.stdout.flush()
    sys.stderr.flush()
