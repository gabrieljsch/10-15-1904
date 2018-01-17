import battlecode as bc

from task_mgmt import task_mgmt


class BlueprintFactory(task_mgmt.Task):
	'''
		Simple Task that constructs a factory blueprint in a given direction
		Arguments: worker, GameController, desired blueprint direction from worker
	'''

	def __init__(self, worker, gc, direction):
		self.built = False
		self.worker = worker.unit
		self.gc = gc
		self.direction = direction
		

	def execute(self):
		if self.gc.can_blueprint(self.worker.id, bc.UnitType.Factory, direction):
			self.gc.blueprint(self.worker.id, bc.UnitType.Factory, direction)
			self.built = True

	def is_done(self):
		return self.built