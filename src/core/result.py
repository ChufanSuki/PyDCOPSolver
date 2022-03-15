from typing import Dict, Set


class Result:
    def __init__(self):
        self.totalCost = 0
        self.messageQuality = 0
        self.totalTime = 0
        self.agentValues: Dict[int, int] = {}
        self.cycleLength = 0
        self.cycleOffset = 0

    def checkFields(self) -> bool:
        flag = True
        cycleLengthFound = 0
        cycleOffsetFound = 0
        try:
            allFields = set()
            for
