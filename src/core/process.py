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
        self.threadName = threadName
        self.isRunning = False
        self.lock = threading.RLock()

    def run(self):
        self.preExecution()
        while True:
            with self.lock:
                if not self.isRunning:
                    break
            self.execution()
        self.postExecution()
        print("Thread " + self.threadName + " terminated")

    def startProcess(self):
        with self.lock:
            if self.isRunning:
                return
            self.isRunning = True
        self.thread = threading.Thread(target=self.run, name=self.threadName)
        self.thread.start()
        print("Thread " + self.threadName + " started")

    def preExecution(self):
        print("Thread " + self.threadName + " is starting")

    def execution(self):
        print("Thread " + self.threadName + " is running")

    def postExecution(self):
        print("Thread " + self.threadName + " stopped")

    def stopProcess(self):
        with self.lock:
            if self.isRunning:
                self.isRunning = False
        print("Thread " + self.threadName + " is terminating")