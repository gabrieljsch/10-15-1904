from nav import Navigator

class MoveTo(Task):
    
    def __init__(self, location, navigator):
        '''Takes a MapLocation and the instance of Navigator'''
        self.loc = location
        self.nav = navigator

    def execute(worker):
        self.direct_unit(worker.unit.id, self.location)

    def is_done(worker):
        return self.nav.still_navigating_unit(worker.unit.id)
