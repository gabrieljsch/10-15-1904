import battlecode as bc
import random
import sys
import traceback

from move_directly import move_directly
from make_factory_at import make_factory_at
from split_robots import split_robots
from worker_ai import worker_ai
from factory_supervisor import factory_supervisor
from gather_k import gather_k
from military_supervisor import military_supervisor


# Template for importing files
from task_mgmt import task_mgmt
from tasks import harvest

gc = bc.GameController()


# A GameController is the main type that you talk to the game with.
# Its constructor will connect to a running game.
# gc = bc.GameController()
directions = list(bc.Direction)

# random.seed(6)

#split units into respective groups
# try:
#     workers, soldiers, factories = split_robots(gc.my_units())
# except:
#     traceback.print_exc()

# create array of worker objects to be mainupplated later
# worker_objects = set([task_mgmt.Worker(worker) for worker in workers])
# for worker_o in worker_objects:
#     worker_o.assign(harvest.Harvest_then_build(worker_o, gc))
#     print('assigned:',worker_o.unit.id)

#make worker object lists
worker_objects = []
factory_objects = []
soldier_objects = []



##All info for kyle's helper functions
#set home_loc and enemy_dir
earth_map = gc.starting_map(bc.Planet.Earth)
x, y = earth_map.width, earth_map.height
started_with_karbonite = []
for x in range(x):
    for y in range(y):
        test_location = bc.MapLocation(bc.Planet.Earth,x,y)
        if earth_map.initial_karbonite_at(test_location) > 0:
            started_with_karbonite.append(test_location)

attack_dir = None
breaker = 0

#set workers needed and factories needed
workers_needed = 1
factories_needed = 1
#home is location of our worker initially
new_loc = gc.my_units()[0].location.map_location()
#find enemy direction
enemy_dir = set_enemy_dir(gc, new_loc)
#then set spaced out home
home_loc = find_home_loc(gc, new_loc, enemy_dir)

#set enemy direction

#Running bot
while True:

    #only run earth
    if gc.planet() is bc.Planet.Earth:


        # split units into respective groups
        worker_objects, factory_objects, soldier_objects,  = split_robots(gc.my_units(), worker_objects, factory_objects, soldier_objects)

        if gc.round() == 1:
            for worker_o in worker_objects:
                worker_o.assign(harvest.Harvest_then_build(worker_o, gc, factory_objects))
                print('assigned:',worker_o.unit.id)

        if gc.round() % 50 == 0:
            print("Round is:", gc.round())




        #main worker loop
        for worker_object in worker_objects:
            if worker_object.task is not None:
                worker_object.work()




    # send the actions we've performed, and wait for our next turn.
    gc.next_turn()

    # these lines are not strictly necessary, but it helps make the logs make more sense.
    # it forces everything we've written this turn to be written to the manager.
    sys.stdout.flush()
    sys.stderr.flush()
