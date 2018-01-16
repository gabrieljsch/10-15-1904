import battlecode as bc
# from main_bot_1 import gc

from task_mgmt import task_mgmt


directions = set(list(bc.Direction))


class Harvest_then_build(task_mgmt.Task):

	def __init__(self, worker, gc):
		self.mined = 0
		self.factory_built = False
		self.worker = worker
		self.gc = gc

	def execute(self):
		if self.mined <= 50:
			for direction in directions:
				if self.gc.can_harvest(self.worker.unit.id, direction):
					self.gc.harvest(self.worker.unit.id, direction)
					self.mined += self.worker.unit.worker_harvest_amount()
					print("Master, I harvested some goods!", self.mined)
					return

			for direction in directions:
				if self.gc.is_move_ready(self.worker.unit.id):
					if self.gc.can_move(self.worker.unit.id, direction):
						self.gc.move_robot(self.worker.unit.id, direction)
		else:
			for direction in directions:
				if self.gc.can_blueprint(self.worker.unit.id, bc.UnitType.Factory, direction):
					self.gc.blueprint(self.worker.unit.id, bc.UnitType.Factory, direction)
					self.factory_built = True
					print("BLUEPRINTED!!!!")
					return


	def is_done(self):
		return self.factory_built








