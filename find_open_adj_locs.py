import battlecode as bc
import random
import sys
import traceback

def find_open_adj_locs(gc, init_loc, unit_to_ignore):

    test_loc = init_loc.clone()

    #make all adjacent squares
    adj_locs = []
    for x_d in [-1,0,1]:
        for y_d in [-1, 0, 1]:
            append_loc = test_loc.clone()
            append_loc = append_loc.translate(x_d, y_d)
            if append_loc != test_loc:
                adj_locs.append(append_loc)

    new_adj_locs = []
    for location in adj_locs:
        if gc.starting_map(bc.Planet.Earth).on_map(location)== True:
            if gc.starting_map(bc.Planet.Earth).is_passable_terrain_at(location) == True:
                if gc.can_sense_location(location) == True:
                    if gc.has_unit_at_location(location) ==True:
                        if gc.sense_unit_at_location(location) == unit_to_ignore:
                            new_adj_locs.append(location)
                    if gc.is_occupiable(location) == True:
                        new_adj_locs.append(location)

    return new_adj_locs
