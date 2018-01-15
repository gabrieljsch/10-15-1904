import battlecode as bc
import random
import sys
import traceback

from make_factory_at import make_factory_at
from make_location import make_location
from gather_k import gather_k

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
            location_for_factory = home_loc

            try:
                if gc.round() >= 100:
                    location_for_factory = home_loc.add(bc.Direction.East)
            except:
                traceback.print_exc()

            need_factory = make_factory_at(gc, builder, location_for_factory, need_factory)
            try:
                for worker in workers:
                    if worker is not workers[0]:
                        gather_k(gc, worker)
            except:
                traceback.print_exc()

            return need_factory
    except:
        traceback.print_exc()
