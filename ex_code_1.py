import battlecode as bc
import random
import sys
import traceback

print("pystarting")

# A GameController is the main type that you talk to the game with.
# Its constructor will connect to a running game.
gc = bc.GameController()
directions = list(bc.Direction)

print("pystarted")

# It's a good idea to try to keep your bots deterministic, to make debugging easier.
# determinism isn't required, but it means that the same things will happen in every thing you run,
# aside from turns taking slightly different amounts of time due to noise.
random.seed(6)

# let's start off with some research!
# we can queue as much as we want.
gc.queue_research(bc.UnitType.Rocket)
gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Knight)

my_team = gc.team()


def move_directly(unit,location_to_go):
    unit_location = unit.location
    map_loc = unit_location.map_location()
    direction_to_go = map_loc.direction_to(location_to_go)
    print("direction to go", direction_to_go)
    print("Robot at", map_loc)

    if unit.movement_heat() < 10:
    #move robot
        try:
            print("unit id", unit.id)
            print(gc.can_move(unit.id,direction_to_go))
            gc.move_robot(unit.id, direction_to_go)
            print("print(did it move?", unit.location)
        except:
            print("actual move failed")
            traceback.print_exc()
            pass

def random_location(unit):
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







while True:
    # We only support Python 3, which means brackets around print()


    try:
        for unit in gc.my_units():
            active_unit = unit

    except:
        traceback.print_exc()
        pass

    try:
        if gc.round() == 1:
            new_location = random_location(unit)


    except Exception as e:
        print('Error:', e)
        # use this to show where the error was
        traceback.print_exc()

    try:
        if gc.round()%30 == 0:
            print('pyround:', gc.round())
            planet = gc.planet()
            try:
                new_location = random_location(unit)
            except:
                pass

    except:
        print("Loc Failed")
        pass


    try:
        move_directly(unit,new_location)
    except:
        print("move Failed")
        traceback.print_exc()
        pass






    # # frequent try/catches are a good idea
    # try:
    #     # walk through our units:
    #     for unit in gc.my_units():
    #
    #         # first, factory logic
    #         if unit.unit_type == bc.UnitType.Factory:
    #             garrison = unit.structure_garrison()
    #             if len(garrison) > 0:
    #                 d = random.choice(directions)
    #                 if gc.can_unload(unit.id, d):
    #                     print('unloaded a knight!')
    #                     gc.unload(unit.id, d)
    #                     continue
    #             elif gc.can_produce_robot(unit.id, bc.UnitType.Knight):
    #                 gc.produce_robot(unit.id, bc.UnitType.Knight)
    #                 print('produced a knight!')
    #                 continue
    #
    #         # first, let's look for nearby blueprints to work on
    #         location = unit.location
    #         if location.is_on_map():
    #             nearby = gc.sense_nearby_units(unit.map_location(), 2)
    #             for other in nearby:
    #                 if gc.can_build(unit.id, other.id):
    #                     gc.build(unit.id, other.id)
    #                     print('built a factory!')
    #                     # move onto the next unit
    #                     continue
    #                 if other.team != my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id):
    #                     print('attacked a thing!')
    #                     gc.attack(unit.id, other.id)
    #                     continue
    #
    #         # okay, there weren't any dudes around
    #         # pick a random direction:
    #         d = random.choice(directions)
    #
    #         # or, try to build a factory:
    #         if gc.karbonite() > bc.UnitType.Factory.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Factory, d):
    #             gc.blueprint(unit.id, bc.UnitType.Factory, d)
    #         # and if that fails, try to move
    #         elif gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
    #             gc.move_robot(unit.id, d)



    # send the actions we've performed, and wait for our next turn.
    gc.next_turn()

    # these lines are not strictly necessary, but it helps make the logs make more sense.
    # it forces everything we've written this turn to be written to the manager.
    sys.stdout.flush()
    sys.stderr.flush()
