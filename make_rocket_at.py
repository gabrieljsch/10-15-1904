import battlecode as bc
import random
import sys
import traceback


from task_mgmt import task_mgmt

from move_directly import move_directly
from build_factory_at import build_factory_at
from find_open_adj_locs import find_open_adj_locs

class Make_rocket_at(task_mgmt.Task):

    def __init__(self, gc, unit_object, rocket_location):
        self.gc = gc
        self.unit_object = unit_object
        self.unit = unit_object.unit
        self.rocket_location = rocket_location
        self.rocket_built = False
        self.destination = None
        print("rocket location", rocket_location)
        if gc.can_sense_location(rocket_location) == True:
            if gc.has_unit_at_location(rocket_location) ==True:
                print("unit there",gc.sense_unit_at_location(rocket_location))
    def execute(self):

        self.unit = self.gc.unit(self.unit.id)
        try:
            destination = find_open_adj_locs(self.gc, self.rocket_location, self.unit)[0]
            self.destination = destination
        except:
            print("No destination?")



        roc_location = self.rocket_location.clone()
        #tests if unit at test space
        location_of_unit = self.unit.location.map_location()
        if location_of_unit.direction_to(self.destination) is bc.Direction.Center:
            #at location
            if self.gc.can_blueprint(self.unit.id, bc.UnitType.Rocket, location_of_unit.direction_to(roc_location)):
                self.gc.blueprint(self.unit.id, bc.UnitType.Rocket, location_of_unit.direction_to(roc_location))
                print("laid print")
            else:
                #changeeeeeee

                build_factory_at(self.gc, self.unit, roc_location)



            if self.gc.can_sense_location(roc_location) == True:
                if self.gc.has_unit_at_location(roc_location) ==True:
                    try:
                        blueprint = self.gc.sense_unit_at_location(roc_location)
                        if blueprint.unit_type == bc.UnitType.Rocket:
                            if blueprint.structure_is_built() == True:
                                self.rocket_built = True
                                print("rocket built")
                    except:
                        traceback.print_exc()


        else:
            try:
                move_directly(self.gc, self.unit, self.destination)
            except:
                traceback.print_exc()



    def is_done(self):
        return self.rocket_built
