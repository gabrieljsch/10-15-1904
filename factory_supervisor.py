import battlecode as bc
import random
import sys
import traceback

from task_mgmt import task_mgmt

class Factory_supervisor(task_mgmt.Task):

    def __init__(self, gc, factory_unit, soldier_objects, worker_objects):
        self.gc = gc
        self.factory_unit = factory_unit
        self. soldier_objects = soldier_objects
        self.worker_objects = worker_objects
        self.robot_built = False

    def execute(self):
        knights_p = 0.0
        mages_p = 0.0
        rangers_p = 1.0
        healer_p = 0.0

        try:
            #if there is a factory

            factory = self.factory_unit.unit
            #if it can produce a ranger
            if self.gc.karbonite()>30:
                if self.gc.can_produce_robot(factory.id, bc.UnitType.Ranger) ==True:
                    try:
                        #and there are less than 7
                        if len(self.worker_objects) == 0:
                            self.gc.produce_robot(factory.id, bc.UnitType.Worker)

                        elif len(self.soldier_objects) < 1000:
                            #do it
                            choice = random.random()
                            if 1.0 -knights_p < choice:
                                self.gc.produce_robot(factory.id, bc.UnitType.Knight)
                            elif 1.0 - knights_p - mages_p < choice:
                                self.gc.produce_robot(factory.id, bc.UnitType.Mage)
                            elif 1.0 - knights_p - mages_p  - rangers_p < choice:
                                self.gc.produce_robot(factory.id, bc.UnitType.Ranger)
                            elif 1.0 - knights_p - mages_p - rangers_p -healers-p < choice:
                                self.gc.produce_robot(factory.id, bc.UnitType.Healer)
                    except:
                        traceback.print_exc()
        except:
            traceback.print_exc()

    def is_done(self):
        return self.robot_built
