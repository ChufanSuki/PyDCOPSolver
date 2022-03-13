"""
Base 'Agent' classes.
An Agent instance is a stand-alone autonomous object. It hosts computations,
which send messages to each other.
Each agent has its own thread, which is used to handle messages as they are
dispatched to computations hosted on this agent.
"""
from typing import Dict, List
from message import Message
import process
class Agent(process.Process):
    def __init__(self, id:int, domain: List[int], neighbours: List[int], constraintCosts: Dict[int, List[List[int]]], neighbourDomains: Dict[int, List[int]]):
        super().__init__("Agent " + str(id))
        self.id = id
        self.domain = domain
        self.neighbours = neighbours
        self.constraintCosts = constraintCosts
        self.neighbourDomains = neighbourDomains
        self.localView = {}
        self.valueIndex = 0

    def preExecution(self):
        for neighbourId in self.neighbours:
            self.localView[neighbourId] = 0
        self.initRun()
        self.postInit()

    def initRun(self):
        pass

    def postInit(self):
        pass

    def runFinished(self):
        pass

    def postExecution(self):
        self.runFinished()

    def sendMessage(self, message: Message):
        pass

    def disposeMessage(self, message: Message):
        pass

    def getLocalCost(self) -> int:
        sum = 0
        for neighbourId in self.neighbours:
            sum += self.constraintCosts[neighbourId][self.valueIndex][self.localView[neighbourId]]
        return sum