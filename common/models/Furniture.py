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

from backend.models import Device, Floor


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
    device = ModelChoiceField(Device.objects, label=_('Device'))

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
