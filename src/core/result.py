from typing import Dict


class Result:
    def __init__(self):
        self.totalCost = 0
        self.messageQuality = 0
        self.totalTime = 0
        self.agentValues: Dict[int, int] = {}
        self.cycleLength = -1
        self.cycleOffset = -1
        if not self.checkFields():
            raise Exception("Result: __init__: checkFields failed due to multiple CycleLength or CycleOffset found!")

    def checkFields(self) -> bool:
        return True
