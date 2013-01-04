import random
from django.forms import HiddenInput
from backend.models.Device import Device
from backend.out import Protocol

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

    def generateRandom(self):
        rand = random.randint(0,67234433)

        unique = True

        for device in self.devices:
            if rand == device.code:
                unique = False

        if not unique:
            return self.generateRandom()
        return rand

    def new(self):
        self.devices = Device.objects.filter(type__startswith='NexaSL')
        self.device.code = self.generateRandom()
        self.device.action = 'on'

    SUPPORTED_ACTIONS = {
        "sync" : sync,
        "on" : on,
        "off" : off,
        }