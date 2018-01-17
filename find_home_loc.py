import battlecode as bc
import random
import sys
import traceback


def find_home_loc(gc, initial_loc,enemy_dir):
    home_loc = None
    test_loc = initial_loc.clone()
    test_loc = test_loc.add(enemy_dir)
    tried = []
    while home_loc is None:
        #make all adjacent squares
        pre_adj_locs = []
        for x_d in [-1,0,1]:
            for y_d in [-1, 0, 1]:
                append_loc = test_loc.clone()
                append_loc = append_loc.translate(x_d, y_d)
                pre_adj_locs.append(append_loc)

        perfect_space = 0
        adj_locs = []
        for location in pre_adj_locs:
            if gc.starting_map(bc.Planet.Earth).on_map(location)== True:
                if gc.starting_map(bc.Planet.Earth).is_passable_terrain_at(location) == True:
                    adj_locs.append(location)
                    perfect_space += 1

        if perfect_space == 9:

            home_loc = test_loc
            return home_loc.subtract(enemy_dir)
        else:
            tried.append(test_loc)
            for loc in adj_locs:
                if loc in tried:
                    adj_locs.remove(loc)
            test_loc = random.choice(adj_locs)
