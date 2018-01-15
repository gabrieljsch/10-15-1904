import battlecode as bc
import random
import sys
import traceback

from make_factory_at import make_factory_at
from make_location import make_location
from gather_k import gather_k

def worker_ai(gc, workers, factories, home_loc, enemy_dir, started_with_karbonite):
    """
    runs the workers of the bots

    input  is gc, list of workers, list of factories, and need factory, which
    is intially 1

    will return 0 when factory count == 1
    """
    try:
        if len(workers) != 0:
            builder = workers[0]
            location_for_factory = home_loc.clone()

            try:
                old_fac = gc.sense_unit_at_location(location_for_factory.add(enemy_dir))
                if old_fac.unit_type is bc.UnitType.Factory:
                    if old_fac.structure_is_built() == True:
                        location_for_factory = location_for_factory.subtract(bc.Direction.West)
            except:
                pass
            make_factory_at(gc, builder, location_for_factory, enemy_dir)

            try:
                for worker in workers:
                    if worker is not workers[0]:
                        gather_k(gc, worker, started_with_karbonite, home_loc)
            except:
                traceback.print_exc()

    except:
        traceback.print_exc()
