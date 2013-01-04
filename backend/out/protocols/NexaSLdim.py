from django.forms import HiddenInput, Widget
import random
from backend.models.Device import Device
from string import Template
from django.utils.safestring import mark_safe
from backend.out import Protocol

class SliderWidget(Widget):
    def render(self, name, value, attrs=None):
        tpl = Template(u'<input name="$name" type="range" class="slider" value="$value" min="0" max="15" />')
        return mark_safe(tpl.substitute(name=name, value=value))

class NexaSLdim(Protocol):
    CONNECTOR_TYPE = "Tellstick"

    CODE_WIDGET = HiddenInput
    ACTION_WIDGET = SliderWidget

    DIM_MIN = 0
    DIM_MAX = 15
    DIM_STEP = 1

    def initialize(self, device):
        assert isinstance(device, Device)
        self.device = device
        self.sender_id = device.code
        self.connector_string = '"protocol":"NEXASL","senderID":"'+self.sender_id+'"'

    def sync(self, **kwargs):
        self.device.connector.object.send(self.connector_string+',"cmd":"on"')

    def on(self, **kwargs):
        try:
            on_level = int(self.device.action)
        except ValueError:
            on_level = 15

        self.dim_level(dim_level=on_level)

    def off(self, **kwargs):
        self.device.connector.object.send(self.connector_string+',"cmd":"off"')

    def dim(self, **kwargs):
        self.device.connector.object.send(self.connector_string+',"cmd":"on"')

    def dim_level(self, **kwargs):
        dim_level = kwargs.get('dim_level')
        self.device.connector.object.send('%s,"cmd":"dim","dimLevel":"%s"' % (self.connector_string, dim_level))

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
        self.device.action = 15

    SUPPORTED_ACTIONS = {
        "sync" : sync,
        "on" : on,
        "off" : off,
        "dim" : dim,
        "dim_level" : dim_level,
        }

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