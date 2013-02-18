from django.db import models
from django.forms import ModelForm, HiddenInput, ModelChoiceField
from backend.models import Thermometer, Floor
from django.utils.translation import ugettext_lazy as _

class Temp(models.Model):
    floor = models.ForeignKey(Floor)
    x = models.IntegerField()
    y = models.IntegerField()
    thermometer = models.ForeignKey(Thermometer)

    class Meta:
        app_label = 'common'

class TempForm(ModelForm):
    thermometer = ModelChoiceField(Thermometer.objects, label=_('Thermometer'))

    class Meta:
        model = Temp
        widgets = {
            'floor': HiddenInput(),
            'x': HiddenInput(),
            'y': HiddenInput(),
            }
