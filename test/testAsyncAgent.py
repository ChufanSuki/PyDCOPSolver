import random
from typing import List, Dict

from core.asyncMailer import AsyncMailer
from core.message import Message
from core.asyncAgent import AsyncAgent


class TestAsyncAgent(AsyncAgent):
    MAX_MESSAGES = 2
    def __init__(self, id: int, domain: List[int], neighbours: List[int], constraintCosts: Dict[int, List[List[int]]], neighbourDomains: Dict[int, List[int]], mailer: AsyncMailer):
        super().__init__(id, domain, neighbours, constraintCosts, neighbourDomains)
        self.currentMessageId = 0

    def initRun(self):
        for neighbourId in self.neighbours:
            self.sendMessage(Message(self.id, neighbourId, self.currentMessageId, None))


    def disposeMessage(self, message: Message):
        print("Agent {} disposeMessage".format(self.id))
        print("Message: {}".format(message))
        if self.currentMessageId >= self.MAX_MESSAGES:
            print("Agent {}: All messages sent".format(self.id))
            self.stopProcess()
            self.currentMessageId += 1
        else:
            self.currentMessageId += 1
            for neighbourId in self.neighbours:
                self.sendMessage(Message(self.id, neighbourId, self.currentMessageId, None))

    def runFinished(self):
        print("Agent {} runFinished".format(self.id))


