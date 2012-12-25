from django.forms import HiddenInput
from backend.models.Device import Device
from backend.out.protocols.Protocol import Protocol

class NexaSLonoff(Protocol):
    CONNECTOR_TYPE = "Tellstick"

    CODE_WIDGET = HiddenInput
    ACTION_WIDGET = HiddenInput

    def initialize(self, device):
        assert isinstance(device, Device)
        self.device = device
        self.sender_id = device.code
        self.connector_string = '"protocol":"NEXASL","senderID":"'+self.sender_id+'"'

    def sync(self, **kwargs):
        self.device.connector.object.send(self.connector_string+',"cmd":"on"')

    def on(self, **kwargs):
        self.device.connector.object.send(self.connector_string+',"cmd":"on"')

    def off(self, **kwargs):
        self.device.connector.object.send(self.connector_string+',"cmd":"off"')

    SUPPORTED_ACTIONS = {
        "sync" : sync,
        "on" : on,
        "off" : off,
        }