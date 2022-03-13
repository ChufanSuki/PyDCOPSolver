import xml.etree.ElementTree as ET
from problem import Problem
from parser import Parser


class ProblemParse:
    BENCHMARK_RANDOM_DCOP = "RandomDCOP"
    TYPE_DCOP = "DCOP"

    def __init__(self, path: str):
        try:
            self.tree = ET.parse(path)
        except:
            print("parse failed")

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
        parser: Parser = Parser()
        if self.getType() == self.TYPE_DCOP:
            if self.getBenchmark() == self.BENCHMARK_RANDOM_DCOP:
                parser = Parser(self.tree.getroot(), problem)
        parser.parseContent()
        return problem
