import xml.etree.ElementTree as ET
from pacman.core.problem import Problem
from pacman.core.parser import Parser


class ProblemParser:
    BENCHMARK_RANDOM_DCOP = "RandomDCOP"
    TYPE_DCOP = "DCOP"

    def __init__(self, path: str):
        self.tree = None
        try:
            self.tree = ET.parse(path)
        except:
            print("parse failed")
            exit(1)

    def getBenchmark(self) -> str:
        root = self.tree.getroot()
        benchmark = root.find("./presentation").attrib['benchmark']
        return benchmark

    def getType(self) -> str:
        root = self.tree.getroot()
        type = root.find("./presentation").attrib['type']
        return type

    def parse(self):
        problem: Problem = Problem()
        parser: Parser = Parser(problem=problem)
        if self.getType() == self.TYPE_DCOP:
            if self.getBenchmark() == self.BENCHMARK_RANDOM_DCOP:
                parser = Parser(self.tree.getroot(), problem)
        parser.parseContent()
        return problem
