import battlecode as bc
import random
import sys
import traceback

def factory_supervisor(gc, factories, soldiers):
    """
    supervises factories. In this case, simply builds a ranger whenever possible



    """
    try:
        #if there is a factory
        if len(factories) != 0:
            #select it
            factory = factories[0]
            #if it can produce a ranger
            if gc.can_produce_robot(factory.id, bc.UnitType.Ranger) ==True:
                try:
                    #and there are less than 7
                    if len(soldiers) < 7:
                        #do it
                        gc.produce_robot(factory.id, bc.UnitType.Ranger)
                except:
                    traceback.print_exc()



    except:
        traceback.print_exc()
