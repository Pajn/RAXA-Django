from backend.models.Device import Device
from backend.out.protocols.Protocol import Protocol

class NexaSC(Protocol):
    CONNECTOR_TYPE = "Tellstick"

    def initialize(self, device):
        assert isinstance(device, Device)
        self.device = device
        house = self.device.code.split('/')[0]
        device = self.device.code.split('/')[1]
        self.connector_string = '"protocol":"NEXASC","house":"'+house+'","device":"'+device+'"'

    def sync(self, **kwargs):
        self.device.connector.object.send(self.connector_string+',"cmd":"on"')

    def on(self, **kwargs):
        self.device.connector.object.send(self.connector_string+',"cmd":"on"')

    def off(self, **kwargs):
        print self.device.connector
        print self.device.connector.object
        self.device.connector.object.send(self.connector_string+',"cmd":"off"')

    def dim(self, **kwargs):
        self.device.connector.object.send(self.connector_string+',"cmd":"on"')

    SUPPORTED_ACTIONS = {
        "sync" : sync,
        "on" : on,
        "off" : off,
        "dim" : dim,
        }