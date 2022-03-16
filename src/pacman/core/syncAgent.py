from typing import Dict, List

from pacman.core.agent import Agent
from pacman.core.message import Message
from pacman.core.syncMailer import SyncMailer


class SyncAgent(Agent):
    def __init__(self, id: int, domain: List[int], neighbours: List[int], constraintCosts: Dict[int, List[List[int]]], neighbourDomains: Dict[int, List[int]], mailer: SyncMailer):
        super().__init__(id, domain, neighbours, constraintCosts, neighbourDomains)
        self.mailer = mailer
        self.mailer.registerAgent(self)
        self.messageQueue: List[Message] = []

    def postInit(self):
        super().postInit()
        self.mailer.agentDone(self.id)

    def addMessage(self, message: Message):
        self.messageQueue.append(message)

    def sendMessage(self, message: Message):
        self.mailer.addMessage(message)

    def execution(self):
        if self.mailer.phase == SyncMailer.PHASE_AGENT and not self.mailer.isDone(self.id):
            while len(self.messageQueue) > 0:
                self.disposeMessage(self.messageQueue.pop(0))
            self.allMessageDisposed()
            self.mailer.agentDone(self.id)

    def allMessageDisposed(self):
        pass