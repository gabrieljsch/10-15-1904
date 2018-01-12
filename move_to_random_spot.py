import battlecode as bc
import random
import sys
import traceback


def move_to_random_spot(gc, unit, on):
    if on == 1:
        try:
            if gc.round() == 1:
                new_location = random_location(gc, unit)


        except Exception as e:
            print('Error:', e)
            # use this to show where the error was
            traceback.print_exc()

        try:
            if gc.round()%30 == 0:
                print('pyround:', gc.round())
                planet = gc.planet()
                try:
                    new_location = random_location(gc, unit)
                except:
                    pass

        except:
            print("Loc Failed")
            pass


        try:
            move_directly(gc, unit,new_location)
        except:
            print("move Failed")
            traceback.print_exc()
            pass
    else:
        pass
