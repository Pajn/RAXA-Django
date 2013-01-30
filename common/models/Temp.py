from django.db import models
from django.forms import ModelForm, HiddenInput
from backend.models import Thermometer, Floor

class Temp(models.Model):
    floor = models.ForeignKey(Floor)
    x = models.IntegerField()
    y = models.IntegerField()
    thermometer = models.ForeignKey(Thermometer)

    class Meta:
        app_label = 'common'

class TempForm(ModelForm):

    class Meta:
        model = Temp
        widgets = {
            'floor': HiddenInput(),
            'x': HiddenInput(),
            'y': HiddenInput(),
            }
