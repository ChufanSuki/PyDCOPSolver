import logging
import threading

# ┌───────────────────────┐
# │    preExeciton        │ P
# │                       │ R
# ├───────────────────────┤ O
# │    execution          │ C
# │                       │ E
# ├───────────────────────┤ S
# │    postExecution      │ S
# │                       │
# └───────────────────────┘
class Process:
    def __init__(self, threadName: str):
        self.suppressOutput = False
        self.threadName = threadName
        self.isRunning = False
        self.lock = threading.RLock()
        self.logger = logging.getLogger('pacman.process')

    def run(self):
        self.preExecution()
        while True:
            with self.lock:
                if not self.isRunning:
                    break
            self.execution()
        self.postExecution()
        if not self.suppressOutput:
            print("Thread " + self.threadName + " terminated")

    def startProcess(self):
        with self.lock:
            if self.isRunning:
                return
            self.isRunning = True
        self.thread = threading.Thread(target=self.run, name=self.threadName)
        self.thread.start()
        self.logger.info("Thread " + self.threadName + " started")

    def preExecution(self):
        self.logger.info("Thread " + self.threadName + " is starting")

    def execution(self):
        self.logger.info("Thread " + self.threadName + " is running")

    def postExecution(self):
        self.logger.info("Thread " + self.threadName + " stopped")

    def stopProcess(self):
        with self.lock:
            if self.isRunning:
                self.isRunning = False
        self.logger.info("Thread " + self.threadName + " is terminating")

    def setSuppressOutpu(self, suppressOutput: bool):
        self.suppressOutput = suppressOutput