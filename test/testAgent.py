from pacman.core.agentManager import AgentManager
from pacman.core.finishedListener import FinishedListener
from pacman.core.problem import Problem
from pacman.core.problemParser import ProblemParser
from pacman.core.resultCycle import ResultCycle

agentDescriptorPath = "/home/dcop/PycharmProjects/Pacman/test/agent.xml"
agentType = "DSA"
problemPath = "/home/dcop/PycharmProjects/Pacman/test/test.xml"

class TestListener(FinishedListener):
    def onFinished(self, result):
        resultCycle: ResultCycle = result
        for i in resultCycle.costIncycle:
            print(i)

if __name__ == "__main__":
    problem: Problem = ProblemParser(problemPath).parse()
    listener = TestListener()
    manager = AgentManager(agentDescriptorPath, agentType, problem, listener)
    manager.startAgents()