'''
Copyright (C) 2013 Rasmus Eneman <rasmus@eneman.eu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import os
import socket
import time
from RAXA.settings import PROJECT_ROOT
from backend.io.connector import Connector, ConnectorNotUsable, ConnectorConnectionError


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
        if not self.is_usable():
            raise ConnectorNotUsable
        string = '{%s,"tellstick":"%s"}' % (string, self.connector.code)
        print string
        self._send('send%s' % string)

    def scan(self):
        self._send('broadcastD')

    def _send(self, message):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', 9001))
            s.send(message)
            s.close()
        except IOError:
            raise ConnectorConnectionError