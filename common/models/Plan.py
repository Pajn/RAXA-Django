from django.db import models
from django.forms import ModelForm, HiddenInput
from backend.models import Room, Floor

class Plan(models.Model):
    floor = models.ForeignKey(Floor)
    x = models.IntegerField()
    y = models.IntegerField()
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    room = models.ForeignKey(Room)

    class Meta:
        app_label = 'common'

class PlanForm(ModelForm):

    class Meta:
        model = Plan
        widgets = {
            'floor': HiddenInput(),
            'x': HiddenInput(),
            'y': HiddenInput(),
            'width': HiddenInput(),
            'height': HiddenInput(),
        }
