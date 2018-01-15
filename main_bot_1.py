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
random.seed(8)

#Running bot
while True:

    #only run earth and red team
    if gc.planet() is bc.Planet.Earth:




        #queue research
        gc.queue_research(bc.UnitType.Ranger)
        # if gc.round()%50 == 0:
        #     print("Factories", factories)


        if gc.round() == 100:
            workers_needed = 3
            factories_needed = 2
        #split units
        try:
            workers, soldiers, factories = split_robots(gc.my_units())
        except:
            traceback.print_exc()


        #set home and enemy locations
        if gc.round()==1:

            #find all squares with Karbonite for the poor workers
            earth_map = gc.starting_map(bc.Planet.Earth)
            x, y = earth_map.width, earth_map.height
            started_with_karbonite = []
            for x in range(x):
                for y in range(y):
                    test_location = bc.MapLocation(bc.Planet.Earth,x,y)
                    if earth_map.initial_karbonite_at(test_location) > 0:
                        started_with_karbonite.append(test_location)
        

            workers_needed = 1
            factories_needed = 1
            #home is location of our worker
            new_loc = workers[0].location.map_location()
            home_loc = new_loc.clone()
            #set locations for neart and far corner
            near_corner, far_corner = bc.MapLocation(bc.Planet.Earth, 1,1), bc.MapLocation(bc.Planet.Earth, 19,19)
            #corner we are furthur from is enemy corner
            #also move our home one closer to enemy
            if home_loc.distance_squared_to(near_corner) > home_loc.distance_squared_to(far_corner):
                enemy_loc = near_corner
            else:
                enemy_loc = far_corner

            enemy_dir = home_loc.direction_to(enemy_loc)
                #set initial values

        try:
            if len(factories) < factories_needed:
                worker_ai(gc, workers, factories, home_loc, enemy_dir, started_with_karbonite)
        except:
            traceback.print_exc()

        try:
            factory_supervisor(gc,factories, soldiers, workers)
        except:
            traceback.print_exc()

        try:
            if len(factories) >= factories_needed:
                if len(workers) != 0:
                    if len(workers) > workers_needed:
                        for worker in workers:
                            gather_k(gc, worker, started_with_karbonite, home_loc)
                    else:
                        try:
                            for worker in workers:
                                if gc.can_replicate(worker.id, bc.Direction.East) == True:
                                    gc.replicate(worker.id, bc.Direction.East)
                        except:
                            traceback.print_exc()
        except:
            traceback.print_exc()

        try:
            military_supervisor(gc, soldiers, factories, enemy_loc, home_loc)
        except:
            traceback.print_exc()



    # send the actions we've performed, and wait for our next turn.
    gc.next_turn()

    # these lines are not strictly necessary, but it helps make the logs make more sense.
    # it forces everything we've written this turn to be written to the manager.
    sys.stdout.flush()
    sys.stderr.flush()
