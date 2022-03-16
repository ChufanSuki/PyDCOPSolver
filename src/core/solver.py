from core.agentManager import AgentManager
from core.finishedListener import FinishedListener
from core.problemParser import ProblemParser


class Solver:
    def solve(self, agentDescriptorPath: str, agentType: str, problemPath: str, listener: FinishedListener):
        parser = ProblemParser(problemPath)
        problem = parser.parse()
        manager = AgentManager(agentDescriptorPath, agentType, problem, listener)
        manager.startAgents()