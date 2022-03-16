from pacman.core.problem import Problem
from pacman.core.problemParser import ProblemParser
problemPath = "/home/dcop/PycharmProjects/Pacman/test/test.xml"
if __name__ == "__main__":
    problem: Problem = ProblemParser(problemPath).parse()
    nb = problem.getNeighbourDomain(1)
    print(problem)