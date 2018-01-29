import battlecode as bc
import random
import sys
import traceback

from make_factory_at import Make_factory_at
from make_location import make_location

def worker_ai(gc, workers, factories, need_factory, home_loc):
    """
    runs the workers of the bots

    input  is gc, list of workers, list of factories, and need factory, which
    is intially 1

    will return 0 when factory count == 1
    """
    try:
        if need_factory == 1:
            builder = workers[0]
            if gc.team() is bc.Team.Red:
                location_for_factory = make_location(gc, 1, 6)
            else:
                location_for_factory = make_location(gc, 19, 13)

            need_factory = make_factory_at(gc, builder, location_for_factory, need_factory)
            return need_factory
    except:
        traceback.print_exc()
