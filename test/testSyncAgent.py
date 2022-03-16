import random
from typing import List, Dict

from core.message import Message
from core.syncAgent import SyncAgent
from core.syncMailer import SyncMailer


class TestSyncAgent(SyncAgent):
    MAX_CYCLE = 2

    def __init__(self, id: int, domain: List[int], neighbours: List[int], constraintCosts: Dict[int, List[List[int]]],
                 neighbourDomains: Dict[int, List[int]], mailer: SyncMailer):
        super().__init__(id, domain, neighbours, constraintCosts, neighbourDomains, mailer)
        self.cycle = 0

    def initRun(self):
        target = self.neighbours[random.randint(0, len(self.neighbours) - 1)]
        self.sendMessage(Message(self.id, target, self.cycle, None))
        print("Agent {} initRun".format(self.id))

    def disposeMessage(self, message: Message):
        print("Agent {} disposeMessage".format(self.id))
        print("Message: {}".format(message))
        target = self.neighbours[random.randint(0, len(self.neighbours) - 1)]
        self.sendMessage(Message(self.id, target, self.cycle, None))

    def allMessageDisposed(self):
        super().allMessageDisposed()
        print("Agent {} allMessageDisposed".format(self.id))
        print("Cycle: {}".format(self.cycle))
        self.sendMessage(Message(self.id, self.id, self.cycle, None))
        self.cycle += 1
        if self.cycle >= TestSyncAgent.MAX_CYCLE:
            self.stopProcess()

    def runFinished(self):
        print("Agent {} runFinished".format(self.id))
