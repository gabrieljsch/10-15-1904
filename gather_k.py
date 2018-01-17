
import battlecode as bc
import random
import sys
import traceback

from task_mgmt import task_mgmt

from move_directly import move_directly

class Gather_k(task_mgmt.Task):

    def __init__(self, gc, worker_object, started_with_karbonite, home_loc):
        self.gc = gc
        self.started_with_karbonite = started_with_karbonite
        self.home_loc = home_loc
        self.worker_object = worker_object
        self.worker = worker_object.unit
        self.done_gathering = False
        
    def execute(self):
        directions = list(bc.Direction)
        if len(self.started_with_karbonite) != 0:
            try:
                first_go = self.started_with_karbonite[0]
                for location in self.started_with_karbonite:
                    worker_loc = self.worker.location.map_location()
                    if worker_loc.distance_squared_to(location) < worker_loc.distance_squared_to(first_go):
                        first_go = location
                    #also remove blank squares?
                    if self.gc.can_sense_location(location) == True:
                        if self.gc.karbonite_at(location) < 1:
                            self.started_with_karbonite.remove(location)

                #if it can harvest do
                if self.gc.can_harvest(self.worker.id, bc.Direction.Center)==True:
                    self.gc.harvest(self.worker.id, bc.Direction.Center)
                else:
                    for direction in directions:
                        if self.gc.can_harvest(self.worker.id, direction)==True:
                            self.gc.harvest(self.worker.id, direction)
                            break
                try:
                    #if it cant, can it move right. If so move
                    move_directly(self.gc, self.worker, first_go)

                except:
                    traceback.print_exc()
            except:
                traceback.print_exc()

    def is_done(self):
        return self.done_gathering
