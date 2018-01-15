from task_mgmt import *
import unittest

class Unit:
    def __init__(self, id):
        self.id = id

class Counter(Task):

    def __init__(self, fr, to, output_list):
        self.count = fr
        self.__to = to
        self.output_list = output_list

    def execute(self, worker):
        self.output_list.append((worker.unit.id, self.count))
        self.count = self.count + 1

    def is_done(self, worker):
        return self.count == self.__to

class TestCounter(unittest.TestCase):

    def test_counter(self):
        worker = Worker(Unit(0))
        output_list = []
        simple_task = Counter(10, 20, output_list)
        worker.assign(simple_task)
        while worker.task is not None:
            worker.work()
        self.assertListEqual(output_list, [(0, i) for i in range(10, 20)])


class Incrementer(Task):
    def __init__(self, num, out):
        self.num = num
        self.done = False
        self.out = out

    def execute(self, worker):
        self.out.append(self.num)
        self.done = True

    def is_done(self, worker):
        return self.done

class CompoundCounter(CompoundTask):
    def __init__(self, fr, to, out):
        super().__init__() # This is important
        tasks = [Incrementer(i, out) for i in range(fr, to)]
        self.task_queue.extend(tasks)

class TestCompoundCounter(unittest.TestCase):
    def test_compound_counter(self):
        worker = Worker(Unit(0))
        output_list = []
        simple_task = CompoundCounter(10, 20, output_list)
        worker.assign(simple_task)
        while worker.task is not None:
            worker.work()
        self.assertListEqual(output_list, list(range(10, 20)))


if __name__ == '__main__':
    unittest.main()
