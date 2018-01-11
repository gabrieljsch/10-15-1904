
def move_directly(unit,location_to_go):
    unit_location = unit.location()
    direction_to_go = unit_location.direction_to(location_to_go)

    if unit.is_move_ready == True:
    #move robot
        try:
            gc.move_robot(1,direction_to_go)
        except:
            pass


def random_location():
    earth_map = gc.starting_map.earth_map

    height, width = earth_map.height, earth_map.weight
    location_x = random.randrange(width)
    location_y = random.randrange(height)
    rand_loc_map = MapLocation(Earth, location_x, location_y)

    return ran_loc_map
