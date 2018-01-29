import battlecode as bc
import random
import sys
import traceback


def find_fac_loc(gc, home_loc):
    fac_loc = None
    test_loc = home_loc.clone()
    # test_loc = test_loc.add(enemy_dir)
    tried = []

    while fac_loc is None:
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
                    if gc.can_sense_location(location) == True:
                        adj_locs.append(location)
                        perfect_space += 1


        if gc.can_sense_location(test_loc) == True:
            if gc.has_unit_at_location(test_loc) == False:
                perfect_space += 1
            else:
                if gc.sense_unit_at_location(test_loc).unit_type is bc.UnitType.Factory:
                    pass
                else:
                    perfect_space += 1

        if perfect_space == 10:

            fac_loc = test_loc
            return fac_loc
        else:
            tried.append(test_loc)
            for loc in adj_locs:
                if loc in tried:
                    adj_locs.remove(loc)
            test_loc = random.choice(adj_locs)
