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

from backend.models import Thermometer, Floor


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
