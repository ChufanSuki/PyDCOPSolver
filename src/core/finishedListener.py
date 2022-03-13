class FinishedListener:
    def __init__(self, finished):
        self.finished = finished

    def onFinished(self, result):
        self.finished(result)