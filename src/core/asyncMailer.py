from datetime import datetime
from typing import List

from core.finishedListener import FinishedListener
from core.message import Message
from core.process import Process
from core.result import Result
from core.asyncAgent import AsyncAgent


class AsyncMailer(Process):
    def __init__(self, finishedListener: FinishedListener= None):
        super().__init__()
        self.listener = finishedListener
        self.messageQueue: List[Message] = []
        self.agents = {}
        self.messageCount = 0
        self.startTime = None
        self.result: Result = Result()

    def registerAgent(self, agent:AsyncAgent):
        self.agents[agent.id] = agent

    def addMessage(self, message: Message):
        with self.messageQueue:
            self.messageQueue.append(message)

    def preExecution(self):
        self.startTime = datetime.now()

    def execution(self):
        with self.lock:
            while len(self.messageQueue) > 0:
                message: Message = self.messageQueue.pop(0)
                if self.agents.get(message.idReceiver).isRunning:
                    self.messageCount += 1
                    self.agents[message.idReceiver].addMessage(message)
            canTerminate = True
            for asyncAgent in self.agents.values():
                if asyncAgent.isRunning:
                    canTerminate = False
                    break

            if canTerminate:
                self.result.messageQuality = self.messageCount
                self.result.totalTime = (datetime.now() - self.startTime).total_seconds()
                if self.listener is not None:
                    self.listener.onFinished(self.result)
                self.stopProcess()


    def setResult(self, id: int, result: Result):
        if self.result is None:
            self.result = result
        else:
            self.result.messageQuality += result.messageQuality
            self.result.agentValues[id] = result.agentValues[id]