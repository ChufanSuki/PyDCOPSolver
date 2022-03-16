import threading


class Process:
    def __int__(self, threadName: str):
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
        print("Thread " + self.threadName + " stopped")

    def startProcess(self):
        with self.lock:
            if self.isRunning:
                return
            self.isRunning = True
        self.thread = threading.Thread(target=self.run, name=self.threadName)
        self.thread.start()

    def preExecution(self):
        pass

    def execution(self):
        pass

    def postExecution(self):
        pass

    def stopProcess(self):
        with self.lock:
            if self.isRunning:
                self.isRunning = False