from __future__ import unicode_literals
from django.forms import HiddenInput, widgets
from backend.models.Device import Device
from backend.out import Protocol

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
        #join = u''.join(rendered_widgets)
        sufix = '</tr></table>'
        block = {0:'a',1:'b',2:'c'}
        i = 0
        join = ''
        for widget in rendered_widgets:
            join = join + '<td>' + widget + '</td>'
            i += 1

        return prefix+join+sufix

    def value_from_datadict(self,data,files,name):
        line_list = [widget.value_from_datadict(data,files,name+'_%s' %i) for i,widget in enumerate(self.widgets)]
        return line_list[0] + '/' + line_list[1]

class NexaSC(Protocol):
    CONNECTOR_TYPE = "Tellstick"

    CODE_WIDGET = CodeSelectWidget
    ACTION_WIDGET = HiddenInput

    def __init__(self):
        super(NexaSC, self).__init__()
        extra_actions = {
            "dim" : self.dim,
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
        self.connector_string = '"protocol":"NEXASC","house":"'+house+'","device":"'+device+'"'

    def sync(self, *args, **kwargs):
        self.device.connector.object.send(self.connector_string+',"cmd":"on"')

    def on(self, *args, **kwargs):
        self.device.connector.object.send(self.connector_string+',"cmd":"on"')

    def off(self, *args, **kwargs):
        print self.device.connector
        print self.device.connector.object
        self.device.connector.object.send(self.connector_string+',"cmd":"off"')

    def dim(self, *args, **kwargs):
        self.device.connector.object.send(self.connector_string+',"cmd":"on"')

    def new(self):
        self.device.action = 'on'
        self.device.code = 'A/1'