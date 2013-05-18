import os
import socket
import time
from RAXA.settings import PROJECT_ROOT
from backend.io.connector import Connector


class Tellstick(Connector):
    TYPE = 'Tellstick'

    def is_usable(self):
        return self.connector.version.startswith('RAXA')

    def update(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 9001))
        s.send('get_ip' + self.connector.code+'\n')
        ip = s.recv(2048)
        s.close()

        path = os.path.join(PROJECT_ROOT, 'other', 'connector.tellstick', 'TellStickNet.hex')

        if ip is not None:
            print 'atftp -p -l %s --tftp-timeout 1 %s' % (path, ip)
            os.system('atftp -p -l %s --tftp-timeout 1 %s' % (path, ip))

        time.sleep(10)

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