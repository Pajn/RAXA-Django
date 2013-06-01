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
import random
from django.forms import HiddenInput
from backend.models.Device import Device
from backend.io.protocol import Protocol


class NexaSLonoff(Protocol):
    CONNECTOR_TYPE = "Tellstick"

    CODE_WIDGET = HiddenInput
    ACTION_WIDGET = HiddenInput

    def __init__(self):
        super(NexaSLonoff, self).__init__()
        extra_actions = {
            "sync": self.sync,
        }
        self.SUPPORTED_ACTIONS.update(extra_actions)

    def initialize(self, device):
        assert isinstance(device, Device)
        self.device = device
        self.sender_id = device.code
        self.connector_string = '"protocol":"NEXASL","senderID":' + self.sender_id

    def sync(self, *args, **kwargs):
        self.device.connector.object.send(self.connector_string + ',"cmd":"on"')

    def on(self, *args, **kwargs):
        self.device.connector.object.send(self.connector_string + ',"cmd":"on"')
        self.device.set_status('on')

    def off(self, *args, **kwargs):
        self.device.connector.object.send(self.connector_string + ',"cmd":"off"')
        self.device.set_status('off')

    def generateRandom(self):
        rand = random.randint(0, 67234433)

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