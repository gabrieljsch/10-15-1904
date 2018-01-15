# buncha imports or whatever
import battlecode as bc
import random
import sys
import traceback
# hardcode some tasks assigned to workers:
task1 = ExampleTask(a, b, c)
worker1 = Worker(example_unit)
worker1.assign(task1)





# init_game
print("pystarting")
# A GameController is the main type that you talk to the game with.
# Its constructor will connect to a running game.
gc = bc.GameController()

print("pystarted")
#set seed
random.seed(8)



# main loop:
while True:


    #run on turn one init
    if gc.round() == 1:
        

    for worker in workers:
        worker.work()

    gc.next_turn()
