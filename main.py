# buncha imports or whatever

# hardcode some tasks assigned to workers:
task1 = ExampleTask(a, b, c)
worker1 = Worker(example_unit)
worker1.assign(task1)

# main loop:
while True:

    for worker in workers:
        worker.work()

    gc.next_turn()
