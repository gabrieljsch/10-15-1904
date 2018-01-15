
import battlecode as bc
import random
import traceback

from move_directly import move_directly
from build_factory_at import build_factory_at



def make_factory_at(gc, worker, factory_location, need_factory):
    """
    gc is game console

    worker is a unit

    factory location is maplocation
    """

    #sets factory location one above given coords
    if gc.team() is bc.Team.Red:
        fac_location = factory_location.add(bc.Direction.North)
    else:
        fac_location = factory_location.add(bc.Direction.South)
    #tests if unit at test space
    try:
        on = 1
        try:
            test_space = gc.sense_unit_at_location(fac_location)
            if test_space.unit_type is bc.UnitType.Factory:
                if test_space.structure_is_built() == False:
                    on = 2
                if test_space.structure_is_built() == True:
                    return 0
        except:
            pass

    except:
        on = 1
        traceback.print_exc()

    if on == 1:
        try:
            move_directly(gc, worker,factory_location)
        except:
            traceback.print_exc()

        try:
            unit = worker
            location_of_unit = unit.location.map_location()

            direction_to_go = location_of_unit.direction_to(factory_location)
            if direction_to_go is bc.Direction.Center:
                if gc.team() is bc.Team.Red:
                    gc.blueprint(worker.id,bc.UnitType.Factory, bc.Direction.North)
                    fac_location = factory_location.add(bc.Direction.North)
                else:
                    gc.blueprint(worker.id, bc.UnitType.Factory, bc.Direction.South)
                    fac_location = factory_location.add(bc.Direction.South)

                should_be_fac = gc.sense_unit_at_location(fac_location)
                if should_be_fac.unit_type == bc.UnitType.Factory:
                    return 1

        except:
            traceback.print_exc()


    if on == 2:
        done = build_factory_at(gc, worker, fac_location,on)
        try:
            blueprint = gc.sense_unit_at_location(fac_location)
            if blueprint.structure_is_built() == True:
                done = 0
        except:
            traceback.print_exc()

        if done == 0:
            need_factory = 0
            return need_factory


    return need_factory
