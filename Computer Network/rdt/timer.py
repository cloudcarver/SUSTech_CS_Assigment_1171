import time
import threading
class timeoutMonitor(threading.Thread):

    def __init__(self, socket, maxTime, sleepTime):
        super().__init__()
        self.socket = socket
        self.start_time = 0
        self.isStart = False
        self.RUN = True
        self.maxTime = maxTime
        self.sleepTime = sleepTime

    def run(self):
        self.start_timer()
        while self.RUN:
            if self.isTimeout():
                self.start_timer()
                self.socket._retransmit()
            time.sleep(self.sleepTime)

    def start_timer(self):
        self.isStart = True
        self.start_time = time.time()

    def stop_timer(self):
        self.isStart = False

    def now(self):
        assert self.isStart == True # The timer haven't been started yet
        return time.time() - self.start_time

    def is_start(self):
        return self.isStart

    def isTimeout(self):
        return self.now() >= self.maxTime

