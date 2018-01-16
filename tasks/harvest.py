import battlecode as bc
# from main_bot_1 import gc

from task_mgmt import task_mgmt


directions = list(bc.Direction)

class Harvest_then_build(task_mgmt.Task):

	def __init__(self, worker):
		self.mined = 0
		self.factory_built = False
		self.worker = worker

	def execute(self):
		if self.mined != 50:
			for direction in directions:
				if gc.can_harvest(worker.id, direction):
					gc.harvest(worker.id, direction)
					self.mined += worker_harvest_amount()
					return
		else:
			for direction in directions:
				if gc.can_build(worker.id, direction):
					gc.build(worker.id, direction)
					self.factory_built = True
					return


	def is_done(self):
		return self.factory_built








