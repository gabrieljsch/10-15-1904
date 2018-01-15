import battlecode as bc
import random
import sys
import traceback


def move_random_after_block(gc, unit):
    directions = list(bc.Direction)

    if gc.is_move_ready(unit.id) ==True:

        try:
            counter = 0
            new_dir = random.choice(directions)
            while gc.can_move(unit.id, new_dir) == False:
                new_dir = random.choice(directions)
                counter +=1
                if counter >8:
                    print("cant move")
                    break
            if gc.can_move(unit.id,new_dir) == True:
                gc.move_robot(unit.id, new_dir)
        except:
            traceback.print_exc()
