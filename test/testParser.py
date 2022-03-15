from core.problem import Problem
from core.problemParser import ProblemParser
problemPath = "/home/dcop/PycharmProjects/Pacman/test/test.xml"
if __name__ == "__main__":
    problem: Problem = ProblemParser(problemPath).parse()
    print(problem)