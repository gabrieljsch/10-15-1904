
import battlecode as bc
import random
import traceback

from move_directly import move_directly
from build_factory_at import build_factory_at



def make_factory_at(gc, unit, factory_location, enemy_dir):
    """
    gc is game console

    worker is a unit

    factory location is maplocation
    """
    
    #sets factory location one above given coords
    builder_location = factory_location.clone()
    fac_location = factory_location.add(enemy_dir)
    #tests if unit at test space

    location_of_unit = unit.location.map_location()

    if location_of_unit.direction_to(builder_location) is bc.Direction.Center:
        #at location
        if gc.can_blueprint(unit.id, bc.UnitType.Factory, enemy_dir):
            gc.blueprint(unit.id, bc.UnitType.Factory, enemy_dir)

        else:
            build_factory_at(gc, unit, fac_location)

    else:
        try:
            move_directly(gc, unit,builder_location)
        except:
            traceback.print_exc()
