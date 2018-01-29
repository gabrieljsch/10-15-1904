import battlecode as bc


def opposite_direction(direction):
	'''
		Given a direction, return the opposite direction in constant time.
	'''
	directions = {
		"Direction.Center" : bc.Direction.Center,
		"Direction.North" : bc.Direction.South,
		"Direction.South" : bc.Direction.North,
		"Direction.East" : bc.Direction.West,
		"Direction.West" : bc.Direction.East,
		"Direction.Northwest" : bc.Direction.Southeast,
		"Direction.Notheast" : bc.Direction.Southwest,
		"Direction.Southwest" : bc.Direction.Northeast,
		"Direction.Southeast" : bc.Direction.Northwest
	}

	return directions[str(direction)]
