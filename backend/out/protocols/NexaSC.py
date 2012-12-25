from django.forms import HiddenInput, TextInput, widgets
from backend.models.Device import Device
from backend.out.protocols.Protocol import Protocol

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

class CodeSelectWidget(widgets.MultiWidget):
    def __init__(self, attrs=None, mode=0):

        _widgets = (
            widgets.Select(attrs=attrs, choices=LETTERS),
            widgets.Select(attrs=attrs, choices=DIGITS),
            )
        super(CodeSelectWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            house = value.split('/')[0]
            device = value.split('/')[1]
            return [house, device]
        return [None, None]

    def format_output(self, rendered_widgets):
        prefix = u'<div class="ui-grid-a">'
        #join = u''.join(rendered_widgets)
        sufix = u'</div>'
        block = {0:'a',1:'b',2:'c'}
        i = 0
        join = ''
        for widget in rendered_widgets:
            join = join + u'<div class="ui-block-' + block[i] + u'">' + widget + u'</div>'
            i += 1

        return prefix+join+sufix

    def value_from_datadict(self,data,files,name):
        print 'Data: ', data
        print 'Files: ', files
        print 'Name: ', name
        line_list = [widget.value_from_datadict(data,files,name+'_%s' %i) for i,widget in enumerate(self.widgets)]
        #try:
        print 'return: ', line_list[0] + '/' + line_list[1]
        return line_list[0] + '/' + line_list[1]
        #except:
        #    return ''

class NexaSC(Protocol):
    CONNECTOR_TYPE = "Tellstick"

    CODE_WIDGET = CodeSelectWidget
    ACTION_WIDGET = HiddenInput

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