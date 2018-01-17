import battlecode as bc

from task_mgmt import task_mgmt


directions = set(list(bc.Direction))


class Harvest_then_build(task_mgmt.Task):

	def __init__(self, worker, gc, factories):
		self.mined = 0
		self.factory_built = False
		self.blueprinted = False
		self.worker = worker
		self.gc = gc
		self.factories = factories

	def execute(self):



		if self.mined <= 50:
			# Try to mine surrounding squares
			for direction in directions:
				if self.gc.can_harvest(self.worker.unit.id, direction):
					self.gc.harvest(self.worker.unit.id, direction)
					self.mined += self.worker.unit.worker_harvest_amount()
					return
			# If can't mine, move to random square if possible
			for direction in directions:
				if self.gc.is_move_ready(self.worker.unit.id):
					if self.gc.can_move(self.worker.unit.id, direction):
						self.gc.move_robot(self.worker.unit.id, direction)
		else:
			# Blueprint / Build the factory
			if not self.blueprinted:
				for direction in directions:
					if self.gc.can_blueprint(self.worker.unit.id, bc.UnitType.Factory, direction):
						self.gc.blueprint(self.worker.unit.id, bc.UnitType.Factory, direction)
						self.blueprinted = True
						print("BLUEPRINTED!!!!", self.worker.unit.id)
						return
			else:
				for factory.unit in self.factories:
					if self.worker.unit.location.is_adjacent_to(factory.location):
						if self.gc.can_build(self.worker.unit.id, factory.id):
							if factory.structure_is_built:
								print("building....", self.worker.unit.id)
								self.gc.build(self.worker.unit.id, factory.id)
								return
						else:
							print("all done m'lord", self.worker.unit.id)
							self.factory_built = True
					else:
						print("Im so confused:", self.worker.unit.id)
						self.factory_built = True



	def is_done(self):
		return self.factory_built
