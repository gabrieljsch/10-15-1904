import battlecode as bc
import random
import sys
import traceback

def factory_supervisor(gc, factories, soldiers, workers):
    """
    supervises factories. In this case, simply builds a ranger whenever possible



    """


    if gc.team() is bc.Team.Red:
        #must == 1
        knights_p = 0.0
        mages_p = 0.0
        rangers_p = 1.0
        healer_p = 0.0
    else:
        knights_p = 0.0
        mages_p = 0.0
        rangers_p = 1.0
        healer_p = 0.0

    try:
        #if there is a factory
        if len(factories) != 0:
            #select it
            for factory in factories:
                #if it can produce a ranger
                if gc.can_produce_robot(factory.id, bc.UnitType.Ranger) ==True:
                    try:
                        #and there are less than 7
                        if len(workers) == 0:
                            gc.produce_robot(factory.id, bc.UnitType.Worker)

                        elif len(soldiers) < 1000:
                            #do it
                            choice = random.random()
                            if 1.0 -knights_p < choice:
                                gc.produce_robot(factory.id, bc.UnitType.Knight)
                            elif 1.0 - knights_p - mages_p < choice:
                                gc.produce_robot(factory.id, bc.UnitType.Mage)
                            elif 1.0 - knights_p - mages_p  - rangers_p < choice:
                                gc.produce_robot(factory.id, bc.UnitType.Ranger)
                                print("Make ranger, carbonite is:",gc.karbonite(),factory.id)
                            elif 1.0 - knights_p - mages_p - rangers_p -healers-p < choice:
                                gc.produce_robot(factory.id, bc.UnitType.Healer)
                    except:
                        traceback.print_exc()



    except:
        traceback.print_exc()
