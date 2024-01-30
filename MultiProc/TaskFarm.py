#
# T a s k F a r m . p y
#

from multiprocessing import Queue, Process
from os import cpu_count


def FuncWrapper(taskFunc, que, procId, taskId, funcArgs):
    result = taskFunc(*funcArgs)
    que.put([procId, [result, taskId]])
    print(f'Message {[procId, [result, taskId]]}')


class TaskFarm(object):
    def __init__(self, taskFunc, numProc=cpu_count()):
        self.numProc = numProc
        self.taskFunc = taskFunc
        self.procTab = [None for _ in range(numProc)]
        self.que = Queue()


    def FreeProc(self):
        procNum = 0;
        while (procNum < self.numProc) and (self.procTab[procNum] != None):
            procNum += 1

        if (procNum < self.numProc):
            return procNum
        else:
            return None


    def NoActiveProc(self):
        return all(map(lambda pTab: pTab == None, self.procTab))


    def StartTask(self, taskId, funcArgs):
        # get free process
        procId = self.FreeProc()

        if (procId == None):
            procId, taskResult = self.que.get()
        else:
            taskResult = None

        # start new task
        self.procTab[procId] = Process(
            target=FuncWrapper, args=(self.taskFunc, self.que, procId, taskId, funcArgs, ))
        self.procTab[procId].start()

        # return result
        return taskResult

    def DrainTask(self):
        if self.NoActiveProc():
            return None

        else:
            procId, taskResult = self.que.get()
            self.procTab[procId] = None

            return taskResult