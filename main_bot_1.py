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

print("pystarting")

# A GameController is the main type that you talk to the game with.
# Its constructor will connect to a running game.
gc = bc.GameController()
directions = list(bc.Direction)

print("pystarted")
random.seed(6)

need_factory = 1
#Running bot
while True:

    #only run earth and red team
    if gc.planet() is bc.Planet.Earth:

        if gc.round()%50 == 0:
            print("Round is:", gc.round())
            print("Karbonite:", gc.karbonite())
            print("Soldiers:", soldiers)
            print("")
            print("Factories", factories)
            print("")
        #set home location



        #split units
        try:
            workers, soldiers, factories = split_robots(gc.my_units())
        except:
            traceback.print_exc()


        #set home and enemy locations

        if gc.round()==1:

            home_loc = workers[0].location.map_location()

            near_corner, far_corner = bc.MapLocation(bc.Planet.Earth, 1,1), bc.MapLocation(bc.Planet.Earth, 19,19)
            if home_loc.distance_squared_to(near_corner) > home_loc.distance_squared_to(far_corner):
                enemy_loc = near_corner
                home_loc = home_loc.add(home_loc.direction_to(near_corner))
            else:
                enemy_loc = far_corner
                home_loc = home_loc.add(home_loc.direction_to(far_corner))

            print("HOMELOC:",home_loc)
            print("enemyloc", enemy_loc)

        #set initial values
        try:
            if need_factory == 1:
                need_factory = worker_ai(gc, workers, factories, need_factory, home_loc)
        except:
            traceback.print_exc()

        try:
            factory_supervisor(gc,factories, soldiers)
        except:
            traceback.print_exc()

        try:
            if need_factory == 0:
                if len(workers) != 0:
                    if len(workers) > 2:
                        for worker in workers:
                            gather_k(gc, worker)
                    else:
                        for worker in workers:
                            if gc.can_replicate(worker.id, bc.Direction.North) == True:
                                gc.replicate(worker.id, bc.Direction.North)
        except:
            traceback.print_exc()

        try:
            military_supervisor(gc, soldiers, factories, enemy_loc)
        except:
            traceback.print_exc()



    # send the actions we've performed, and wait for our next turn.
    gc.next_turn()

    # these lines are not strictly necessary, but it helps make the logs make more sense.
    # it forces everything we've written this turn to be written to the manager.
    sys.stdout.flush()
    sys.stderr.flush()
