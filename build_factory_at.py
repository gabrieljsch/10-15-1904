import battlecode as bc
import random
import sys
import traceback


from move_directly import move_directly


def build_factory_at(gc, worker, fac_location):
    """
    Subfunction of make_factory, uses a worker to build up factory
    after blueprint is laid

    """
    #get the blueprint just laid

    if gc.can_sense_location(fac_location) == True:
        if gc.has_unit_at_location(fac_location) ==True:
            try:
                blueprint = gc.sense_unit_at_location(fac_location)

            except:
                traceback.print_exc()

            #try to build on blueprint
            try:
                if gc.can_build(worker.id, blueprint.id):
                    #if not fully built
                    if blueprint.structure_is_built() == False:
                        #build
                        gc.build(worker.id, blueprint.id)
                        
            except:
                traceback.print_exc()
