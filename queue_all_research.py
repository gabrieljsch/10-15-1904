import battlecode as bc
import random
import sys
import traceback


def queue_all_research(gc):
    """queues all research for the game on round one"""
    gc.queue_research(bc.UnitType.Worker)
    gc.queue_research(bc.UnitType.Rocket)
    gc.queue_research(bc.UnitType.Ranger)
    gc.queue_research(bc.UnitType.Ranger)
    gc.queue_research(bc.UnitType.Ranger)
