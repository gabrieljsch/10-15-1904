import battlecode as bc
import random
import sys
import traceback

from split_robots import split_robots

def on_first_turn(gc):
    split_robots(gc.my_units())
    
