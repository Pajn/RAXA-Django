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
from django.db import models
from django.forms import ModelForm, HiddenInput, ModelChoiceField
from django.utils.translation import ugettext_lazy as _

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
        return self.width / 2 + self.x

    @property
    def center_y(self):
        return self.height / 2 + self.y

    class Meta:
        app_label = 'common'


class PlanForm(ModelForm):
    room = ModelChoiceField(Room.objects, label=_('Room'))

    class Meta:
        model = Plan
        widgets = {
            'floor': HiddenInput(),
            'x': HiddenInput(),
            'y': HiddenInput(),
            'width': HiddenInput(),
            'height': HiddenInput(),
        }
