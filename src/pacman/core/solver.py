from pacman.core.agentManager import AgentManager
from pacman.core.finishedListener import FinishedListener
from pacman.core.problemParser import ProblemParser


class Solver:
    def solve(self, agentDescriptorPath: str, agentType: str, problemPath: str, listener: FinishedListener):
        parser = ProblemParser(problemPath)
        problem = parser.parse()
        manager = AgentManager(agentDescriptorPath, agentType, problem, listener)
        manager.startAgents()