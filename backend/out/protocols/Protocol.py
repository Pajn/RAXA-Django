from backend.models.Device import Device

class Protocol(object):
    CONNECTOR_TYPE = ''

    def initialize(self, device):
        assert isinstance(device, Device)
        self.device = device

    def sync(self):
        raise NotImplementedError

    def on(self):
        raise NotImplementedError

    def off(self):
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