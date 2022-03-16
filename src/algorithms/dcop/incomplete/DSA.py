"""
Distributed Stochastic Algorithm
DSA is a synchronous stochastic local search algorithm that works on a constraints graph. At startup, each variable takes a random value from it’s domain and then run the same procedure in repeated steps.

At each step, each variable send its value to its neighbors. Once a variable has received the value from all it’s neighbors, it evaluates the gain it could obtain by picking another value. If this gain is positive, it decides to change it’s value or to keep the current one. This decision is made stochastically: a variable change its value with probability p (if doing so can improve the state quality).

The algorithm stops after a predefined number of steps.
"""
import random
import sys
from typing import List, Dict

from core.message import Message
from core.resultCycle import ResultCycle
from core.syncAgent import SyncAgent
from core.syncMailer import SyncMailer


class DSA(SyncAgent):
    MSG_VALUE = 1
    p = 1.0
    DSA_ROUND = 1000

    def __init__(self, id: int, domain: List[int], neighbours: List[int], constraintCosts: Dict[int, List[List[int]]], neighbourDomains: Dict[int, List[int]], mailer: SyncMailer):
        super().__init__(id, domain, neighbours, constraintCosts, neighbourDomains, mailer)
        self.cycle = 0

    def initRun(self):
        self.valueIndex = random.randint(0, len(self.domain) - 1)
        self.broadcastValueMsg()

    def broadcastValueMsg(self):
        for i in self.neighbours:
            self.sendMessage(Message(self.id, i, self.MSG_VALUE, self.valueIndex))

    def runFinished(self):
        cycle = ResultCycle()
        cycle.totalCost = self.getLocalCost() * 1.0 / 2
        cycle.agentValues[self.id] = 0
        self.mailer.setResultCycle(self.id, cycle)

    def selectBestValue(self) -> int:
        minCost = sys.maxsize
        minValue = -1
        for i in range(0, len(self.domain)):
            localCost = 0
            for nId in self.neighbours:
                localCost += self.constraintCosts[nId][self.valueIndex][self.localView[nId]]
            if minCost < localCost:
                minCost = localCost
                minValue = i
        return minValue

    def allMessageDisposed(self):
        super().allMessageDisposed()
        self.cycle += 1
        if self.cycle < self.DSA_ROUND:
            if random.random() < self.p:
                bestValue = self.selectBestValue()
                if self.valueIndex != self.bestValue:
                    self.valueIndex = bestValue
                    self.broadcastValueMsg()
        else:
            self.stopProcess()

    def disposeMessage(self, message: Message):
        if message.type == self.MSG_VALUE:
            sendId = message.idSender
            self.localView[sendId] = message.value
