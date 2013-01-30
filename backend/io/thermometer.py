import os
import time

def supported_types():
    dir = os.path.join(os.path.dirname(__file__), 'thermometers')
    types = []
    for file in os.listdir(dir):
        if file.endswith('.py'):
            if file != '__init__.py':
                types.append(file[:-3])

    return types

def get_class(thermometer):
    tmpmodule = __import__('backend.io.thermometers.%s' % thermometer, fromlist=[thermometer])
    tmpclass = getattr(tmpmodule, thermometer)
    return tmpclass

def scan_thermometers():
    types = supported_types()
    for type in types:
        get_class(type)().scan()
    time.sleep(10)

class Thermometer(object):
    TYPE = ''

    def initialize(self, thermometer):
        self.thermometer = thermometer

    def scan(self):
        pass