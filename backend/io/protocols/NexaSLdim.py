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
from string import Template

from django.forms import HiddenInput, Widget
from django.utils.safestring import mark_safe

from backend.models.Device import Device
from backend.io.protocol import DimLevelProtocol


class SliderWidget(Widget):
    def render(self, name, value, attrs=None):
        tpl = Template(u'<input name="$name" type="range" class="slider" value="$value" min="0" max="15" />')
        return mark_safe(tpl.substitute(name=name, value=value))


class NexaSLdim(DimLevelProtocol):
    CONNECTOR_TYPE = "Tellstick"

    CODE_WIDGET = HiddenInput
    ACTION_WIDGET = SliderWidget

    DIM_MIN = 0
    DIM_MAX = 15
    DIM_STEP = 1

    def __init__(self):
        super(NexaSLdim, self).__init__()
        extra_actions = {
            "sync": self.sync,
            "dim": self.dim,
            "dim_level": self.dim_level,
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
        try:
            on_level = int(self.device.action)
        except ValueError:
            on_level = 15

        self.dim_level(dim_level=on_level)

    def off(self, *args, **kwargs):
        self.device.connector.object.send(self.connector_string + ',"cmd":"off"')
        self.device.set_status('off')

    def dim(self, *args, **kwargs):
        self.device.connector.object.send(self.connector_string + ',"cmd":"on"')
        self.device.set_status('dim')

    def dim_level(self, *args, **kwargs):
        dim_level = kwargs.get('dim_level')
        self.device.connector.object.send('%s,"cmd":"dim","dimLevel":%s' % (self.connector_string, dim_level))
        self.device.set_status(dim_level)

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
        self.device.action = 15