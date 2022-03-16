import threading
from datetime import datetime

from pacman.core.finishedListener import FinishedListener
from pacman.core.message import Message
from pacman.core.process import Process
from pacman.core.resultCycle import ResultCycle
# from core.syncAgent import SyncAgent


class SyncMailer(Process):
    PHASE_AGENT = 1
    PHASE_MAILER = 2
    def __init__(self, finishedListerner: FinishedListener = None):
        super().__init__("mailer")
        self.agentReady_lock = threading.RLock()
        self.messageQueue_lock = threading.RLock()
        self.phase_lock = threading.RLock()
        self.resultCycle = None
        self.agents = {}
        self.messageQueue = []
        self.agentReady = {}
        self.phase = self.PHASE_AGENT
        self.costInCycle = [0, 0]
        self.listener = finishedListerner
        self.messageCount = 0
        self.tail = 0
        self.agentReady= set()
        self.stoppedAgents = set()
        self.cycleCount = 0

    def expand(self):
        tmpCostInCycle = [0 for i in range(self.costInCycle.__len__() * 2)]
        for i in range(self.costInCycle.__len__()):
            tmpCostInCycle[i] = self.costInCycle[i]
        self.costInCycle = tmpCostInCycle

    def registerAgent(self, agent):
        self.agents[agent.id] = agent

    def addMessage(self, message: Message):
        with self.phase_lock:
            while self.phase == self.PHASE_MAILER:
                continue
            with self.messageQueue_lock:
                self.messageQueue.append(message)

    def preExecution(self):
        self.startTime = datetime.now()

    def execution(self):
        if self.phase == self.PHASE_MAILER:
            with self.messageQueue_lock:
                while self.messageQueue.__len__() > 0:
                    message = self.messageQueue.pop(0)
                    self.messageCount = self.messageCount + 1
                    if self.agents[message.idReceiver].isRunning:
                        self.agents[message.idReceiver].addMessage(message)
                    else:
                        pass
                    canTerminate = True
                    cost = 0
                    for syncAgent in self.agents.values():
                        if syncAgent.isRunning:
                            canTerminate = False
                        else:
                            self.stoppedAgents.add(syncAgent)
                        cost = cost + syncAgent.getLocalCost()
                    cost = cost / 2
                    if self.tail == self.costInCycle.__len__() - 1:
                        self.expand()
                    self.costInCycle[self.tail+1] = cost
                    self.tail = self.tail + 1
                    if canTerminate:
                        self.stopProcess()
                    else:
                        self.cycleCount = self.cycleCount + 1
                        self.agentReady = set()
                        self.phase = self.PHASE_AGENT


    def agentDone(self, id: int):
        with self.agentReady_lock:
            self.agentReady.add(id)
            if self.agentReady.__len__() == self.agents.__len__() - self.stoppedAgents.__len__():
                self.phase = self.PHASE_MAILER

    def isDone(self, id: int):
        return self.agentReady.__contains__(id)

    def setResultCycle(self, id: int, resultCycle: ResultCycle):
        if self.resultCycle == None:
            self.resultCycle = resultCycle
        else:
            self.resultCycle.add(resultCycle)
            self.resultCycle.agentValues[id] = resultCycle.agentValues[id]
        if self.resultCycle.agentValues.keys().__len__() == self.agents.__len__():
            self.resultCycle.totalTime = datetime.now() - self.startTime
            self.resultCycle.messageQuality = self.messageCount
            self.resultCycle.setCostInCycle(self.costInCycle, self.tail)
            if self.listener != None:
                self.listener.onFinished(self.resultCycle)

