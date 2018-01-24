
import battlecode as bc
import random
import traceback

from task_mgmt import task_mgmt

from move_directly import move_directly
from build_factory_at import build_factory_at
from find_open_adj_locs import find_open_adj_locs

class Make_factory_at(task_mgmt.Task):

    def __init__(self, gc, unit_object, factory_location):
        self.gc = gc
        self.unit_object = unit_object
        self.unit = unit_object.unit
        self.factory_location = factory_location
        self.factory_built = False
        self.destination = None

    def execute(self):

        self.unit = self.gc.unit(self.unit.id)
        try:
            destination = find_open_adj_locs(self.gc, self.factory_location, self.unit)[0]
            self.destination = destination
        except:
            print("No destination?")



        fac_location = self.factory_location.clone()
        #tests if unit at test space
        location_of_unit = self.unit.location.map_location()
        if location_of_unit.direction_to(self.destination) is bc.Direction.Center:
            #at location
            if self.gc.can_blueprint(self.unit.id, bc.UnitType.Factory, location_of_unit.direction_to(fac_location)):
                self.gc.blueprint(self.unit.id, bc.UnitType.Factory, location_of_unit.direction_to(fac_location))
            else:
                build_factory_at(self.gc, self.unit, fac_location)



            if self.gc.can_sense_location(fac_location) == True:
                if self.gc.has_unit_at_location(fac_location) ==True:
                    try:
                        blueprint = self.gc.sense_unit_at_location(fac_location)

                        if blueprint.structure_is_built() == True:
                            self.factory_built = True
                    except:
                        traceback.print_exc()


        else:
            try:
                move_directly(self.gc, self.unit, self.destination)
            except:
                traceback.print_exc()





        #sets factory location one above given coords


    def is_done(self):
        return self.factory_built
