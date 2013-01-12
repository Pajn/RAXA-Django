import os

def supported_types():
    dir = os.path.join(os.path.dirname(__file__), 'protocols')
    types = []
    for file in os.listdir(dir):
        if file.endswith('.py'):
            if file != '__init__.py':
                types.append((file[:-3], file[:-3]))

    return types

def get_class(connector):
    tmpmodule = __import__('backend.out.protocols.%s' % connector, fromlist=[connector])
    tmpclass = getattr(tmpmodule, connector)
    return tmpclass

class Protocol(object):
    CONNECTOR_TYPE = ''

    def __init__(self):
        self.SUPPORTED_ACTIONS = {
            "sync" : self.sync,
            "on" : self.on,
            "off" : self.off,
            "toggle" : self.toggle,
            }

    def initialize(self, device):
        self.device = device

    def sync(self, *args, **kwargs):
        raise NotImplementedError

    def on(self, *args, **kwargs):
        raise NotImplementedError

    def off(self, *args, **kwargs):
        raise NotImplementedError

    def toggle(self, *args, **kwargs):
        if self.is_off():
            self.on()
        else:
            self.off()

    def new(self):
        pass

    def action(self, **kwargs):
        action = kwargs.get('action')
        if action is '':
            action = self.device.action
        self.SUPPORTED_ACTIONS[action](self, **kwargs)

    def is_off(self):
        if self.device.status == 'off':
            return True
        else:
            return False

class DimLevelProtocol(Protocol):
    DIM_MIN = 0
    DIM_MAX = 1
    DIM_STEP = 1

    def action(self, **kwargs):
        action = kwargs.get('action')
        if action is '':
            action = self.device.action
        try:
            dim_level = int(action)
            action = 'dim_level'
            kwargs['dim_level'] = dim_level
        except ValueError:
            pass
        self.SUPPORTED_ACTIONS[action](self, **kwargs)

    def getSteps(self):
        steps = []
        for step in range(self.DIM_MIN, self.DIM_MAX, self.DIM_STEP):
            steps.append(step)
        return steps