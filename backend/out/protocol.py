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

    def initialize(self, device):
        self.device = device

    def sync(self):
        raise NotImplementedError

    def on(self):
        raise NotImplementedError

    def off(self):
        raise NotImplementedError

    def new(self):
        raise NotImplementedError

    SUPPORTED_ACTIONS = {
        "sync" : sync,
        "on" : on,
        "off" : off,
        }

    def action(self, **kwargs):
        action = kwargs.get('action')
        if action is '':
            action = self.device.action
        self.SUPPORTED_ACTIONS[action](self, **kwargs)