import socket
import time
from backend.io.connector import Connector

class Tellstick(Connector):
    TYPE = 'Tellstick'

    def __init__(self):
        self.connect()

    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(('127.0.0.1', 9001))

    def send(self, string):
        string = '{%s,"tellstick":"%s"}' % (string, self.connector.code)
        print string
        self._send('send%s' % string)

    def scan(self):
        self._send('broadcastD')

    def _send(self, message):
        sent = self.s.send(message)
        if sent == 0:
            self.connect()
            self.s.send(message)