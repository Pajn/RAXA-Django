from django.db import models
from django.forms import ModelForm, HiddenInput
from backend.models import Device, Floor

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

class Furniture(models.Model):
    types = {
        'dot': 0,
    }
    type = models.PositiveSmallIntegerField(default=types['dot'])
    floor = models.ForeignKey(Floor)
    x1 = models.IntegerField()
    y1 = models.IntegerField()
    x2 = models.IntegerField(default=0)
    y2 = models.IntegerField(default=0)
    device = models.ForeignKey(Device)

    class Meta:
        app_label = 'common'

class FurnitureForm(ModelForm):

    class Meta:
        model = Furniture
        widgets = {
            'type': HiddenInput(),
            'floor': HiddenInput(),
            'x1': HiddenInput(),
            'y1': HiddenInput(),
            'x2': HiddenInput(),
            'y2': HiddenInput(),
        }
