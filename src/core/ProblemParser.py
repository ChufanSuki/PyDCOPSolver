import xml.etree.ElementTree as ET


class ProblemParse:
    BENCHMARK_RANDOM_DCOP = "RandomDCOP"
    TYPE_DCOP = "DCOP"

    def __init__(self, path: str):
        try:
            self.tree = ET.parse(path)
        except:
            print("parse failed")

    def parse(self):
        problem: problem.Problem = problem.Problem()
