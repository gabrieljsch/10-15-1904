import battlecode as bc
import random
import sys
import traceback


def random_location(gc, unit):
    try:

        unit_location = unit.location
        new_location = unit_location.clone()
        map_loc = new_location.map_location()

        print("map_loc",map_loc)
        earth = gc.planet()
        print(earth)
        earth_map = gc.starting_map(earth)

        height, width = earth_map.height, earth_map.width
        location_x = random.randrange(width)
        location_y = random.randrange(height)

        print("locxy",location_x,location_y)
        map_loc.x = location_x
        map_loc.y = location_y
        # map_loc.x = 2
        # map_loc.y = 2
        print(map_loc.x)
        print(map_loc)

        print ("Old loc:", unit_location)
        print ("New loc:",map_loc)
        return map_loc

    except:
        print("Rand earth fail")
        traceback.print_exc()
