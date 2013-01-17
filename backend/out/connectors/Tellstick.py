import socket
import time
from backend.out import Connector

class Tellstick(Connector):
    TYPE = 'Tellstick'

    def send(self, string):
        string = '{%s,"tellstick":"%s"}' % (string, self.connector.code)
        print string
        self._send('send%s' % string)

    def scan(self):
        self._send('broadcastD')

    def _send(self, message):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 9001))
        s.send(message)
        s.close()
        time.sleep(0.5)