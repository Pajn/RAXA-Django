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
    tmpmodule = __import__('backend.out.connectors.%s' % connector, fromlist=[connector])
    tmpclass = getattr(tmpmodule, connector)
    return tmpclass

def scan_connectors():
    types = supported_types()
    for type in types:
        get_class(type)().scan()
    time.sleep(10)

class Connector(object):
    TYPE = ''

    def initialize(self, connector):
        self.connector = connector

    def send(self, string):
        raise NotImplementedError

    def scan(self):
        pass