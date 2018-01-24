import battlecode as bc
import random
import sys
import traceback

from set_enemy_dir import set_enemy_dir
from find_home_loc import find_home_loc

def on_turn_one(gc):
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
    workers_needed = 4
    factories_needed = 1
    #home is location of our worker initially
    my_units = gc.my_units()
    if len(my_units) != 0:
        new_loc = my_units[0].location.map_location()
    #find enemy direction
    enemy_dir = set_enemy_dir(gc, new_loc)
    #then set spaced out home
    home_loc = find_home_loc(gc, new_loc, enemy_dir)

    #set enemy direction
    print("enemy_dir",enemy_dir)
    print()
    print("home_loc", home_loc)
    return started_with_karbonite, attack_dir, breaker, workers_needed, factories_needed, enemy_dir, home_loc
