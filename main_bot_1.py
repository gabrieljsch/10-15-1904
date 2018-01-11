import battlecode as bc
import random
import sys
import traceback

from move_directly import move_directly
from random_location import random_location

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
            new_location = random_location(gc, unit)


    except Exception as e:
        print('Error:', e)
        # use this to show where the error was
        traceback.print_exc()

    try:
        if gc.round()%30 == 0:
            print('pyround:', gc.round())
            planet = gc.planet()
            try:
                new_location = random_location(gc, unit)
            except:
                pass

    except:
        print("Loc Failed")
        pass


    try:
        move_directly(gc, unit,new_location)
    except:
        print("move Failed")
        traceback.print_exc()
        pass

    # send the actions we've performed, and wait for our next turn.
    gc.next_turn()

    # these lines are not strictly necessary, but it helps make the logs make more sense.
    # it forces everything we've written this turn to be written to the manager.
    sys.stdout.flush()
    sys.stderr.flush()
