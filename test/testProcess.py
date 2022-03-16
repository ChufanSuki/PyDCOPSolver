from core.process import Process
processList = []
NUM_PROCESSES = 2
for i in range(2):
    process = Process("process" + str(i))
    processList.append(process)

for process in processList:
    process.startProcess()