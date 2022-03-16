from datetime import datetime
from typing import List

# from core import asyncAgent
from pacman.core.finishedListener import FinishedListener
from pacman.core.message import Message
from pacman.core.process import Process
from pacman.core.result import Result

class AsyncMailer(Process):
    def __init__(self, finishedListener: FinishedListener= None):
        super().__init__("mailer")
        self.listener = finishedListener
        self.messageQueue: List[Message] = []
        self.agents = {}
        self.messageCount = 0
        self.startTime = None
        self.result: Result = Result()

    def registerAgent(self, agent):
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