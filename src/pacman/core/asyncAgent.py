from typing import List, Dict

from pacman.core import asyncMailer
from pacman.core.agent import Agent
from pacman.core.message import Message


class AsyncAgent(Agent):
    def __init__(self, id: int, domain: List[int], neighbours: List[int], constraintCosts: Dict[int, List[List[int]]], neighbourDomains: Dict[int, List[int]], mailer: asyncMailer.AsyncMailer):
        super().__init__(id, domain, neighbours, constraintCosts, neighbourDomains)
        self.mailer = mailer
        self.mailer.registerAgent(self)
        self.messageQueue = []

    def sendMessage(self, message: Message):
        self.mailer.addMessage(message)

    def addMessage(self, message: Message):
        with self.messageQueue:
            self.messageQueue.append(message)

    def execution(self):
        tmpQueue = []
        with self.lock:
            while len(self.messageQueue) > 0:
                tmpQueue.append(self.messageQueue.pop(0))
        while len(tmpQueue) > 0:
            self.disposeMessage(tmpQueue.pop(0))
