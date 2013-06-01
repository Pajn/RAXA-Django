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
from __future__ import unicode_literals
from string import Template
from django.forms import Widget
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from backend.models.Device import Device
from backend.models.Scenario import Scenario


class DeviceScenario(Widget):
    def __init__(self, value=None, *args, **kwargs):
        super(DeviceScenario, self).__init__(*args, **kwargs)

        self.value = value

        self.devices = Device.objects.all()
        self.scenarios = Scenario.objects.all()

    def render_device_option(self, selected, device):
        SELECTED = ''
        if selected:
            SELECTED = 'selected="selected"'

        tpl = Template('''<option value="D/$id" $selected>$name</option>''')
        return mark_safe(tpl.safe_substitute(id=device.id,
                                             selected=SELECTED, name=device.name))

    def render_scenario_option(self, selected, scenario):
        SELECTED = ''
        if selected:
            SELECTED = 'selected="selected"'

        tpl = Template('''<option value="S/$id" $selected>$name</option>''')
        return mark_safe(tpl.safe_substitute(id=scenario.id,
                                             selected=SELECTED, name=scenario.name))

    def render_options(self, value):
        is_device = False
        is_scenario = False
        try:
            id = value.id
            if isinstance(value, Device):
                is_device = True
            elif isinstance(value, Scenario):
                is_scenario = True
        except AttributeError:
            id = ''

        options = '<optgroup label="%s">' % _('Devices')
        for device in self.devices:
            if is_device and id == device.id:
                selected = True
            else:
                selected = False
            options += self.render_device_option(selected, device)
        options += '</optgroup><optgroup label="%s">' % _('Scenarios')
        for scenario in self.scenarios:
            if is_scenario and id == scenario.id:
                selected = True
            else:
                selected = False
            options += self.render_scenario_option(selected, scenario)
        options += '</optgroup>'

        return options

    def render(self, name, value, attrs=None):
        options = self.render_options(self.value)
        if 'disabled' in self.attrs:
            disabled = 'disabled="disabled"'
        else:
            disabled = ''

        attrs = disabled

        tpl = Template('''<select name="$name" $attrs>$options</select>''')

        return mark_safe(tpl.safe_substitute(name=name, attrs=attrs, options=options))

    def value_from_datadict(self, data, files, name):
        value = data[name]
        value = value.split('/')

        if value[0] == 'D':
            id = value[1]
            device = Device.objects.get(pk=id)
            return device
        elif value[0] == 'S':
            id = value[1]
            scenario = Scenario.objects.get(pk=id)
            return scenario
        else:
            return None


class DeviceScenarioHidden(DeviceScenario):
    is_hidden = True

    def __init__(self, value=None, *args, **kwargs):
        super(DeviceScenarioHidden, self).__init__(*args, **kwargs)

        try:
            id = value.id
            if isinstance(value, Device):
                self.value = 'D/%s' % id
            elif isinstance(value, Scenario):
                self.value = 'S/%s' % id
        except AttributeError:
            self.value = ''

    def render(self, name, value, attrs=None, choices=()):

        tpl = Template('''<input type="hidden" name="$name" value="$value" />''')

        return mark_safe(tpl.safe_substitute(name=name, value=self.value))