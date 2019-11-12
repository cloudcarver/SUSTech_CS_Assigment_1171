from socket import *
import random, time

class UDPsocket(socket):
    def __init__(self, loss_rate=0.2, corruption_rate=0.2, delay_rate=0.2, delay=1):
        super().__init__(AF_INET, SOCK_DGRAM)
        self.loss_rate = loss_rate
        self.corruption_rate = corruption_rate
        self.delay_rate = delay_rate
        self.delay = delay
        self.timeout_value = 0.5

    def settimeout(self, value):
        self.timeout_value = value

    def recvfrom(self, bufsize):
        data, addr = super().recvfrom(bufsize)
        if random.random() < self.loss_rate:
            return None
        if random.random() < self.corruption_rate:
            return self._corrupt(data), addr
        if random.random() < self.delay_rate:
            time.sleep(self.timeout_value)
        return data, addr

    def recv(self, bufsize):
        data, addr = self.recvfrom(bufsize)
        return data

    def _corrupt(self, data: bytes) -> bytes:
        raw = list(data)
        for i in range(0, random.randint(0, 3)):
            pos = random.randint(0, len(raw) - 1)
            raw[pos] = random.randint(0, 255)
        return bytes(raw)
