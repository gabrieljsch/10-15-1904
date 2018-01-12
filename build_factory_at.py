import battlecode as bc
import random
import sys
import traceback


from move_directly import move_directly


def build_factory_at(gc, worker, location_of_factory, on):
    """
    Subfunction of make_factory, uses a worker to build up factory
    after blueprint is laid

    input on is odd and hacky, basically comes in as 2 and stays 2 unit structure is
    built, at which point it returns as 2
    """
    #get the blueprint just laid
    blueprint = gc.sense_unit_at_location(location_of_factory)

    #try to build on blueprint
    try:
        if gc.can_build(worker.id, blueprint.id):
            #if not fully built
            if blueprint.structure_is_built() == False:
                #build
                gc.build(worker.id, blueprint.id)

        #if built, indicate by returing 0
        if blueprint.structure_is_built() == True:
            return 0

    except:
        traceback.print_exc()
        
    #continue by returning 2
    return 2
