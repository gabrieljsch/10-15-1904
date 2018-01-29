from abc import ABC, abstractmethod
from collections import deque

# This is a way to create new tasks and assign them to workers.
# A higher level strategic AI should generate and prioritize these tasks.



class Worker:
    '''Workers are assigned tasks and perform them to completion or
    until interrupted.'''
    def __init__(self, unit):
        '''Create a new worker from given unit.'''
        self.unit = unit
        self.task = None

    def assign(self, task):
        if self.task is not None:
            print("Reassigning worker", self.unit.id,
                  "from", type(self.task), "to", type(task))
        self.task = task

    def work(self):
        if self.task is not None:
            if self.task.is_done():
                self.free()
            else:
                self.task.execute()
                if self.task.is_done():
                    self.free()
        else:
            print("Worker", self.unit.id, "has no assigned task!")

    def free(self):
        self.task = None

class WorkerPool:
    '''Gives access to working and free workers. Can be sorted by
    distance and/or priority of worker task (TODO).'''
    # TODO: Give a way to automatically shuffle workers when
    # reprioritizing tasks
    pass
    
# note for Gabe and Kyle: This class is an "abstract class", which
# means it cannot be instantiated directly and is therefore only for
# subclassing from. In effect, any object that inherits from Task can
# be treated like a Task (e.g., can have execute() called on it) and
# must implement all of Task's methods. However, each different type
# of task can have different constructors, different attributes (e.g.,
# task-specific coordinates), and behave differently.
class Task(ABC):

    @abstractmethod
    def execute(self, worker):
        '''Run the instructions in this Task'''
        pass

    @abstractmethod
    def is_done(self, worker):
        '''Returns true when this task is complete. Normally true when the
        task queue is empty, or possibly when a termination condition
        is satisfied.'''
        pass

class CompoundTask(Task):
    ''' '''
    def __init__(self):
        # Task_queue is a structure that consists of other tasks.
        # Tasks are executed until they are done, and then they are
        # removed from the task_queue. 
        self.task_queue = deque()

    def execute(self, worker):
        # Processes the task queue 
        if self.task_queue:
            task = self.task_queue[0]
            task.execute(worker)
            
            if task.is_done(worker):
                # clear any completed tasks and clean up if we're
                # completely done
                self.task_queue.popleft()
                while self.task_queue:
                    task = self.task_queue[0]
                    # remove this task if it's done
                    if task.is_done(worker):
                        # remove the task from the task_queue
                        self.task_queue.popleft()                
                    else:
                        break
        else:
            print('This task should have already been removed!')

    def is_done(self, worker):
        return len(self.task_queue) == 0

class ExampleCompoundTask(CompoundTask):

    def __init__(self, location, navigator):
        self.location = location
        self.task_queue.extend([MoveTo(location, navigator),
                                DoOtherThing()])
        
        
# thought: what happens if an assigned worker can no longer complete
# its assigned task (e.g., because it's blocked)?

# another thought: workers should prioritize their own safety when
# possible (or have it prioritized for them...)
