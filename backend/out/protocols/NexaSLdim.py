from django.forms import HiddenInput, Widget
from backend.models.Device import Device
from backend.out.protocols.Protocol import Protocol
from string import Template
from django.utils.safestring import mark_safe

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
        dim_level = kwargs.get('instance')
        self.device.connector.object.send(self.connector_string+',"cmd":"dim","dimLevel":"'+dim_level+'"')

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
            action = "dim_level"
        except ValueError:
            pass
        self.SUPPORTED_ACTIONS[action](self, **kwargs)