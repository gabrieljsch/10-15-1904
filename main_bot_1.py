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
from find_home_loc import find_home_loc
from set_enemy_dir import set_enemy_dir

print("pystarting")

# A GameController is the main type that you talk to the game with.
# Its constructor will connect to a running game.
gc = bc.GameController()
directions = list(bc.Direction)


print("pystarted")
random.seed(12)


#Running bot
while True:

    #only run earth and red team
    if gc.planet() is bc.Planet.Earth:
        #queue research
        gc.queue_research(bc.UnitType.Ranger)
        # if gc.round()%50 == 0:
        #     print("Factories", factories)




        # if gc.round()%20 == 0:
        #     print("Round:", gc.round())
        #     print("attack_dir", attack_dir)
        #     print("Time left:", gc.get_time_left_ms())


        if gc.round() == 100:
            workers_needed = 3
            factories_needed = 2

        if gc.round() > 300:
            if gc.round()%50 == 0:
                rand_d= random.choice(directions)
                if rand_d != bc.Direction.Center:
                    attack_dir = rand_d
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

            attack_dir = None
            breaker = 0


            #set workers needed and factories needed
            workers_needed = 1
            factories_needed = 1
            #home is location of our worker initially
            new_loc = workers[0].location.map_location()
            #find enemy direction
            enemy_dir = set_enemy_dir(gc, new_loc)
            #then set spaced out home
            home_loc = find_home_loc(gc, new_loc, enemy_dir)

            #set enemy direction


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
                                for direction in directions:
                                    if gc.can_replicate(worker.id, direction) == True:
                                        gc.replicate(worker.id, direction)

                        except:
                            traceback.print_exc()
        except:
            traceback.print_exc()

        try:
            full_unit_seen_list = military_supervisor(gc, soldiers, factories, enemy_dir, home_loc, attack_dir)
            #look into factories#
            #TODO move out of main
            if breaker == 0:
                if full_unit_seen_list != None:
                    if len(full_unit_seen_list) != 0:
                        for enemy in full_unit_seen_list:
                            if enemy.unit_type == bc.UnitType.Factory:
                                attack_dir = home_loc.direction_to(enemy.location.map_location())
                                breaker = 1

        except:
            traceback.print_exc()



    # send the actions we've performed, and wait for our next turn.
    gc.next_turn()

    # these lines are not strictly necessary, but it helps make the logs make more sense.
    # it forces everything we've written this turn to be written to the manager.
    sys.stdout.flush()
    sys.stderr.flush()
