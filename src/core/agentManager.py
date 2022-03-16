import time

from core.agent import Agent
from core.agentParser import AgentParser
from core.asyncMailer import AsyncMailer
from core.finishedListener import FinishedListener
from core.problem import Problem
from core.syncMailer import SyncMailer


class AgentManager:
    METHOD_ASYNC = "ASYNC"
    METHOD_SYNC = "SYNC"

    def __init__(self, agentDescriptorPath: str, agentType: str, problem: Problem, listener: FinishedListener):
        self.agent = []
        self.agentDescriptors = AgentParser(agentDescriptorPath).parse()
        descriptor = self.agentDescriptors[agentType.upper()]
        if descriptor.method == AgentManager.METHOD_ASYNC:
            self.asyncMailer = AsyncMailer(listener)
        else:
            self.syncMailer = SyncMailer(listener)
        for id in problem.allId:
            agent: Agent = None
            try:
                agent = Agent(id, problem.domains[id], problem.neighbours[id], problem.constraintCost[id], problem.getNeighbourDomain(id),  self.syncMailer == None if self.syncMailer else self.asyncMailer)
            except Exception as e:
                print(e)
            self.agent.append(agent)


    def startAgents(self):
        for agent in self.agent:
            agent.startProcess()
        try:
            time.sleep(200)
        except KeyboardInterrupt:
            print("Keyboard interrupt")
        if self.asyncMailer:
            self.asyncMailer.startProcess()
        elif self.syncMailer:
            self.syncMailer.startProcess()
