from typing import List

from core.result import Result


class ResultCycle(Result):
    def __init__(self, costIncycle: List[float] = []):
        super().__init__()
        self.costIncycle = costIncycle

    def setCostInCycle(self, costIncycle: List[float], tail: int):
        self.costIncycle = [costIncycle[i] for i in range(tail)]