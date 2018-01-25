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
from make_rocket_at import Make_rocket_at

# Template for importing files
from task_mgmt import task_mgmt
from tasks import harvest

print("running")
gc = bc.GameController()


# A GameController is the main type that you talk to the game with.
# Its constructor will connect to a running game.
# gc = bc.GameController()
directions = list(bc.Direction)

random.seed(6)


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
        #  and gc.team() is bc.Team.Red:


        # split units into respective groups
        worker_objects, factory_objects, soldier_objects, unbuilt_structures, rockets = split_robots(gc.my_units(), worker_objects, factory_objects, soldier_objects, gc)
        all_objects = worker_objects+ factory_objects+ soldier_objects

        #worker controls

        #if we dont have enough workers but have 1
        if len(worker_objects) != 0 and len(worker_objects)<= workers_needed:
            for worker_object in worker_objects:
                worker = worker_object.unit.id
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
                    builder.assign(Make_factory_at(gc, builder, find_fac_loc(gc, home_loc)))
            else:
                if builder.task is None:
                    builder.assign(Gather_k(gc, builder, started_with_karbonite, home_loc))

        if gc.research_info().get_level(bc.UnitType.Rocket) >=1:
            if len(rockets) == 0:
                if len(worker_objects) >1 :
                    rocket_man = worker_objects[0]
                    if rocket_man.task is None:
                        rocket_man.assign(Make_rocket_at(gc,rocket_man, find_fac_loc(gc, rocket_man.unit.location.map_location())))
                        print("build that rocket")


        #if nothing else, build then gather
        if gc.round() > 1:
            for worker_o in worker_objects:
                if worker_o.task is None and worker_o != worker_objects[0]:
                    if len(unbuilt_structures)> 0:
                        if unbuilt_structures[0].unit_type == bc.UnitType.Factory:
                            try:
                                worker_o.assign(Make_factory_at(gc, worker_o, unbuilt_structures[0].location.map_location()))
                            except:
                                print("can't make factory")
                        if unbuilt_structures[0].unit_type == bc.UnitType.Rocket:
                            try:
                                worker_o.assign(Make_rocket_at(gc, worker_o, unbuilt_structures[0].location.map_location()))
                            except:
                                print("cant make rocket")
                    else:
                        worker_o.assign(Gather_k(gc, worker_o, started_with_karbonite, home_loc))

        #try building a rocket




        #factory_controls
        if len(factory_objects) !=0:
            for factory in factory_objects:
                if factory.task is None:
                    factory.assign(Factory_supervisor(gc, factory, soldier_objects, worker_objects))


        #soldier controllers
        if len(soldier_objects) > 0:
            soldier_objects = military_supervisor(gc, soldier_objects, factory_objects, enemy_dir, home_loc, attack_dir)


        #check printng loop
        if gc.round() % 100 == 0:
            print("Round is:", gc.round())
            print("rockets", rockets)
            print("unbuilt_objects", unbuilt_structures)

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
