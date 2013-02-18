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

    @property
    def center_x(self):
        return self.width/2 + self.x

    @property
    def center_y(self):
        return self.height/2 + self.y

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
