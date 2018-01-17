import battlecode as bc
import random
import traceback

def soldier_move(gc, unit, units_seen, enemy_dir, home_loc, attack_dir):
    """
    move soldiers at where the enemy likely is, and updates that spot
    also provides speard

    """
    directions_pre = [bc.Direction.North, bc.Direction.Northeast, bc.Direction.East, bc.Direction.Southeast, bc.Direction.South, bc.Direction.Southwest, bc.Direction.West, bc.Direction.Northwest]
    directions = directions_pre+directions_pre


    if attack_dir != None:
        attack_dir = enemy_dir
    #if we can move
    if gc.is_move_ready(unit.id) ==True:
        #TODO
        #check if we know where factories are
        for enemy in units_seen:
            if enemy.unit_type == bc. UnitType.Factory:
                enemy_dir = home_loc.direction_to(enemy.location.map_location())


        #set weights
        front_p = .15
        front_left_p, front_right_p = .15, .15
        right_p, left_p = .2, .2,
        back_right_p, back_left_p = .05, .05
        back_p = 0.05

        #name directions based on enemy_dir
        i_f = directions.index(enemy_dir)
        front, front_right, right, back_right = directions[i_f], directions[i_f+1], directions[i_f+2], directions[i_f+3]
        back, back_left, left, front_left = directions[i_f+4], directions[i_f +5], directions[i_f+6], directions[i_f+7]

        #choose random and choose
        counter = 0
        while counter < 8:
            choice = random.random()
            if 1.0 - front_p < choice:
                direction_chosen = front
            elif 1.0 - front_p - front_left_p < choice:
                direction_chosen = front_left
            elif 1.0 - front_p - front_left_p- front_right_p < choice:
                direction_chosen = front_right
            elif 1.0 - front_p - front_left_p- front_right_p -left_p < choice:
                direction_chosen = left
            elif 1.0 - front_p - front_left_p- front_right_p -left_p -right_p< choice:
                direction_chosen = right
            elif 1.0 - front_p - front_left_p- front_right_p -left_p -right_p - back_right_p < choice:
                direction_chosen = back_right
            elif 1.0 - front_p - front_left_p- front_right_p -left_p -right_p - back_right_p - back_left_p< choice:
                direction_chosen = back_left
            elif 1.0 - front_p - front_left_p- front_right_p -left_p -right_p - back_right_p - back_left_p-  back_p< choice:
                direction_chosen = back


            if gc.can_move(unit.id, direction_chosen)==True:
                gc.move_robot(unit.id, direction_chosen)
                counter = 10
            counter +=1

    return enemy_dir



        #try moving that way
