from datetime import time


class Message:
    def __int__(self, idSender: int, idReceiver: int, type: int, value):
        self.idSender = idSender
        self.idReceiver = idReceiver
        self.type = type
        self.value = value

    def __str__(self):
        return "Message: idSender: {}, idReceiver: {}, type: {}, value: {}".format(self.idSender, self.idReceiver, self.type, self.value)