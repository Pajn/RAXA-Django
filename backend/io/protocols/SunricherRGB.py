import socket
from string import Template
from django.forms import Widget, TextInput
from django.utils.safestring import mark_safe
import time
from backend.models.Device import Device
from backend.io.protocol import Protocol

class ColorWheelWidget(Widget):
    def render(self, name, value, attrs=None):
        tpl = Template(
            u'''<div style="position: relative; width: 200px; height: 200px;">
                <img src="/static/images/color_wheel.png"
                     style="position: absolute; top: 0px; left: 0px; width: 200px; height: 200px;"
                     onload="$(this).click(function(e) {
                         var offset = $(this).offset();
                         var x = e.clientX - offset.left;
                         var y = e.clientY - offset.top;
                         var x_diff = x - 100;
                         var y_diff = y - 100;
                         var angle = (180 * Math.atan(x_diff/y_diff)) / Math.PI;
                         if (y_diff < 0) { angle += 180; }
                         else if (x_diff < 0 && y_diff > 0) { angle += 360; }
                         var angle = Math.floor(angle);
                         $(this).next().next('input').val('CW'+angle);
                     });"/>
                <img src="/static/images/white.png"
                     style="position: absolute; top: 62px; left: 62px; width: 76px; height: 76px;"
                     onclick="$(this).next('input').val('white')"/>
                <input type="hidden" name="$name" value="$value" />
            </div>''')
        return mark_safe(tpl.safe_substitute(name=name, value=value))

class SunricherRGB(Protocol):
    CONNECTOR_TYPE = None

    CODE_WIDGET = TextInput
    ACTION_WIDGET = ColorWheelWidget

    def __init__(self):
        super(SunricherRGB, self).__init__()
        extra_actions = {
            "color_wheel" : self.color_wheel,
            "white" : self.white,
            }
        self.SUPPORTED_ACTIONS.update(extra_actions)

    def initialize(self, device):
        assert isinstance(device, Device)
        self.device = device
        self.ip = device.code

    def on(self, *args, **kwargs):
        data = bytearray.fromhex('02 00 02 12 ab')
        self._send(data, self.ip, 8899)
        self.device.set_status('on')

    def off(self, *args, **kwargs):
        data = bytearray.fromhex('02 00 02 12 a9')
        self._send(data, self.ip, 8899)
        self.device.set_status('off')

    def color_wheel(self, *args, **kwargs):
        # On
        data = bytearray.fromhex('02 00 02 12 ab')
        self._send(data, self.ip, 8899)
        time.sleep(0.2)

        angle = int(kwargs.get('angle'))
        angle = int (1.0 + (4.0 * angle) / 15.0)
        if angle < 5:
            angle += 92
        else:
            angle += -4
        angle = '%0.2X' % angle
        data = bytearray.fromhex('02 00 01 01 %s' % angle)
        self._send(data, self.ip, 8899)
        self.device.set_status('CW%s' % int(kwargs.get('angle')))

    def white(self, *args, **kwargs):
        # On
        data = bytearray.fromhex('02 00 02 12 ab')
        self._send(data, self.ip, 8899)
        time.sleep(0.2)
        # Blue
        data = bytearray.fromhex('02 00 02 03 87')
        self._send(data, self.ip, 8899)
        time.sleep(0.1)
        # Green
        data = bytearray.fromhex('02 00 02 03 84')
        self._send(data, self.ip, 8899)
        time.sleep(0.1)
        # Red
        data = bytearray.fromhex('02 00 02 03 81')
        self._send(data, self.ip, 8899)
        self.device.set_status('white')

    def new(self):
        self.device.action = 'on'

    def action(self, *args, **kwargs):
        action = kwargs.get('action')
        if action.startswith('CW'):
            kwargs['angle'] = action[2:]
            kwargs['action'] = 'color_wheel'
        super(SunricherRGB, self).action(**kwargs)

    def _send(self, data, ip, port):
        datarow = bytearray.fromhex(u'55 39 38 32')
        datarow.insert(4, data[0])
        datarow.insert(5, data[1])
        datarow.insert(6, data[2])
        datarow.insert(7, data[3])
        datarow.insert(8, data[4])
        datarow.insert(9, (data[0] + data[1] + data[2] + data[3] + data[4]) & 0x0000ff)
        datarow.insert(10, 0xAA)
        datarow.insert(11, 0xAA)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        print(''.join("0x%0.2X" % byte for byte in datarow))
        s.sendall(datarow)
        s.close()