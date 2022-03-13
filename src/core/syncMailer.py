from datetime import datetime
from typing import Set

from core.finishedListener import FinishedListener
from core.message import Message
from core.process import Process
from core.resultCycle import ResultCycle
from core.syncAgent import SyncAgent


class SyncMailer(Process):
    PHASE_AGENT = 1
    PHASE_MAILER = 2
    def __init__(self, finishedListerner: FinishedListener = None):
        super().__init__()
        self.resultCycle = None
        self.agents = {}
        self.messageQueue = []
        self.agentReady = {}
        self.phase = self.PHASE_AGENT
        self.costInCycle = [0, 0]
        self.listener = finishedListerner
        self.messageCount = 0
        self.tail = 0
        self.agentReady: Set= set()

    def expand(self):
        tmpCostInCycle = [0 for i in range(self.costInCycle.__len__() * 2)]
        for i in range(self.costInCycle.__len__()):
            tmpCostInCycle[i] = self.costInCycle[i]
        self.costInCycle = tmpCostInCycle

    def register(self, agent: SyncAgent):
        self.agents[agent.id] = agent

    def addMessage(self, message: Message):
        with self.phase:
            while self.phase == self.PHASE_MAILER:
                continue
            with self.messageQueue:
                self.messageQueue.append(message)

    def preExecution(self):
        self.startTime = datetime.now()

    def execution(self):
        if self.phase == self.PHASE_MAILER:
            with self.messageQueue:
                while self.messageQueue.__len__() > 0:
                    message = self.messageQueue.pop(0)
                    self.messageCount = self.messageCount + 1
                    if self.agents[message.getIdReceiver()].isRunning():
                        self.agents[message.getIdReceiver()].addMessage(message)
                    else:
                        pass
                    canTerminate = True
                    cost = 0
                    for syncAgent in self.agents.values():
                        if syncAgent.isRunning():
                            canTerminate = False
                        cost = cost + syncAgent.getCost()
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
        with self.agentReady:
            self.agentReady.add(id)
            if self.agentReady.__len__() == self.agents.__len__():
                self.phase = self.PHASE_MAILER

    def isDone(self, id: int):
        return self.agentReady.__contains__(id)

    def setResultCycle(self, id: int, resultCycle: ResultCycle):
        if self.resultCycle == None:
            self.resultCycle = resultCycle
        else:
            self.resultCycle.add(resultCycle)
            self.reultCycle.setAgentValues(id, resultCycle.getAgentValue(id))
        if self.resultCycle.getAgents().__len__() == self.agents.__len__():
            self.resultCycle.setTotalTime(datetime.now() - self.startTime)
            self.resultCycle.setMessageQuality(self.messageCount)
            self.resultCycle.setCostInCycle(self.costInCycle, self.tail)
            if self.listener != None:
                self.listener.onFinished(self.resultCycle)

