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
import time


def supported_types():
    dir = os.path.join(os.path.dirname(__file__), 'connectors')
    types = []
    for file in os.listdir(dir):
        if file.endswith('.py'):
            if file != '__init__.py':
                types.append(file[:-3])

    return types


def get_class(connector):
    tmpmodule = __import__('backend.io.connectors.%s' % connector, fromlist=[connector])
    tmpclass = getattr(tmpmodule, connector)
    return tmpclass


def scan_connectors():
    types = supported_types()
    for type in types:
        get_class(type)().scan()
    time.sleep(5)


class Connector(object):
    TYPE = ''

    def initialize(self, connector):
        self.connector = connector

    def is_usable(self):
        return False

    def update(self):
        raise NotImplementedError

    def scan(self):
        pass