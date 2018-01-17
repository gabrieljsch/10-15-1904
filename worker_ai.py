import battlecode as bc
import random
import sys
import traceback

from make_factory_at import make_factory_at
from make_location import make_location
from gather_k import gather_k
from find_open_adj_locs import find_open_adj_locs
from move_directly import move_directly
from build_factory_at import build_factory_at

def worker_ai(gc, workers, factories, home_loc, enemy_dir, started_with_karbonite):
    """
    runs the workers of the bots

    input  is gc, list of workers, list of factories, and need factory, which
    is intially 1

    will return 0 when factory count == 1
    """
    try:
        if len(workers) != 0:
            # have inital worker lay blueprint
            builder = workers[0]
            location_for_factory = home_loc.clone()
            #this is the code to make the second factory
            try:
                #if there is a factory at our home loc (should be)
                old_fac = gc.sense_unit_at_location(location_for_factory.add(enemy_dir))
                if old_fac.unit_type is bc.UnitType.Factory:
                    if old_fac.structure_is_built() == True:
                        #make location one to East
                        location_for_factory = location_for_factory.subtract(bc.Direction.West)
            except:
                pass
            #now build factory at that location, with worker 1
            make_factory_at(gc, builder, location_for_factory, enemy_dir)

            try:
                #make other workers do shit
                counter = 0
                for worker in workers:
                    destinations = find_open_adj_locs(gc, location_for_factory.add(enemy_dir), worker)
                    if worker is not workers[0]:
                        try:
                            destination = destinations[counter]
                            if worker.location.map_location() not in destinations:
                                try:
                                    move_directly(gc, worker, destination)
                                except:
                                    traceback.print_exc()

                            if worker.location.map_location() in destinations:
                                try:
                                    build_factory_at(gc, worker, location_for_factory.add(enemy_dir))
                                except:
                                    traceback.print_exc()

                            counter +=1
                        except:
                            traceback.print_exc()




                        # gather_k(gc, worker, started_with_karbonite, home_loc)
            except:
                traceback.print_exc()

    except:
        traceback.print_exc()
