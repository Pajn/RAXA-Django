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
from __future__ import unicode_literals
from django.forms import HiddenInput, widgets
from backend.models.Device import Device
from backend.io.protocol import Protocol


class CodeSelectWidget(widgets.MultiWidget):
    LETTERS = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
        ('G', 'G'),
        ('H', 'H'),
        ('I', 'I'),
        ('J', 'J'),
        ('K', 'K'),
        ('L', 'L'),
        ('M', 'M'),
        ('N', 'N'),
        ('O', 'O'),
        ('P', 'P'),
    )

    DIGITS = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11),
        (12, 12),
        (13, 13),
        (14, 14),
        (15, 15),
        (16, 16),
    )

    def __init__(self, attrs=None, mode=0):
        _widgets = (
            widgets.Select(attrs=attrs, choices=self.LETTERS),
            widgets.Select(attrs=attrs, choices=self.DIGITS),
        )
        super(CodeSelectWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            house = value.split('/')[0]
            device = value.split('/')[1]
            return [house, device]
        return [None, None]

    def format_output(self, rendered_widgets):
        prefix = '<table style="display:inline-table; margin: 0; padding: 0; border 0; border-spacing: 0;"><tr>'
        sufix = '</tr></table>'
        join = ''
        for widget in rendered_widgets:
            join = join + '<td>' + widget + '</td>'

        return prefix + join + sufix

    def value_from_datadict(self, data, files, name):
        line_list = [widget.value_from_datadict(data, files, name + '_%s' % i) for i, widget in enumerate(self.widgets)]
        return line_list[0] + '/' + line_list[1]


class NexaSC(Protocol):
    CONNECTOR_TYPE = "Tellstick"

    CODE_WIDGET = CodeSelectWidget
    ACTION_WIDGET = HiddenInput

    LETTERS = {
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3,
        'E': 4,
        'F': 5,
        'G': 6,
        'H': 7,
        'I': 8,
        'J': 9,
        'K': 10,
        'L': 11,
        'M': 12,
        'N': 13,
        'O': 14,
        'P': 15,
    }

    def __init__(self):
        super(NexaSC, self).__init__()
        extra_actions = {
            "sync": self.sync,
            "dim": self.dim,
        }
        self.SUPPORTED_ACTIONS.update(extra_actions)

    def initialize(self, device):
        assert isinstance(device, Device)
        self.device = device
        if self.device.code.split('/').__len__() == 2:
            house = self.device.code.split('/')[0]
            device = self.device.code.split('/')[1]
        else:
            house = 'A'
            device = '1'
        house = self.LETTERS.get(house)
        device = int(device) - 1
        self.connector_string = '"protocol":"NEXASC","house":{0},"device":{1}'.format(house, device)

    def sync(self, *args, **kwargs):
        self.device.connector.object.send(self.connector_string + ',"cmd":"on"')

    def on(self, *args, **kwargs):
        self.device.connector.object.send(self.connector_string + ',"cmd":"on"')
        self.device.set_status('on')

    def off(self, *args, **kwargs):
        self.device.connector.object.send(self.connector_string + ',"cmd":"off"')
        self.device.set_status('off')

    def dim(self, *args, **kwargs):
        self.device.connector.object.send(self.connector_string + ',"cmd":"on"')
        self.device.set_status('dim')

    def new(self):
        self.device.action = 'on'
        self.device.code = 'A/1'