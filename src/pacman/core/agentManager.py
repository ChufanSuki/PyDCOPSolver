import time

from pacman.core.agent import Agent
from pacman.core.agentParser import AgentParser
from pacman.core.asyncMailer import AsyncMailer
from pacman.core.finishedListener import FinishedListener
from pacman.core.problem import Problem
from pacman.core.syncMailer import SyncMailer
import importlib

class AgentManager:
    METHOD_ASYNC = "ASYNC"
    METHOD_SYNC = "SYNC"

    def __init__(self, agentDescriptorPath: str, agentType: str, problem: Problem, listener: FinishedListener):
        self.agents = []
        self.agentDescriptors = AgentParser(agentDescriptorPath).parse()
        descriptor = self.agentDescriptors[agentType.upper()]
        if descriptor.method == AgentManager.METHOD_ASYNC:
            self.asyncMailer = AsyncMailer(listener)
        else:
            self.syncMailer = SyncMailer(listener)
        for id in problem.allId:
            agent: Agent = None
            try:
                moudle_name = importlib.import_module("pacman.algorithms.dcop.incomplete.dsa")
                # TODO: Change to a variable
                # moudle_name = importlib.import_module("pacman.algorithms.dcop.incomplete.testSync")
                class_name = getattr(moudle_name, descriptor.className)
                agent = class_name(id, problem.domains[id], problem.neighbours[id], problem.constraintCost[id], problem.getNeighbourDomain(id),  self.syncMailer  if self.syncMailer is not None else self.asyncMailer)
            except Exception as e:
                print(e)
                exit(1)
            self.agents.append(agent)


    def startAgents(self):
        for agent in self.agents:
            agent.startProcess()
        try:
            time.sleep(200)
        except KeyboardInterrupt:
            print("Keyboard interrupt")
        if hasattr(self, "asyncMailer"):
            self.asyncMailer.startProcess()
        elif hasattr(self, "syncMailer"):
            self.syncMailer.startProcess()
