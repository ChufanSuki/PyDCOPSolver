from core.finishedListener import FinishedListener
from core.process import Process


class AsyncMailer(Process):
    def __init__(self, finishedListener: FinishedListener):
        super().__init__()
        self.listener = finishedListener
        self.messageQueue = []
        self.agents = {}
        self.messageCount = 0
        self.startTime = 0
        self.result = None
