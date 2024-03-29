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
from django.core.exceptions import ValidationError
from django.utils.encoding import force_unicode
from django import forms
from django.utils.translation import ugettext_lazy as _
from automation.models import LogicBlock
from automation.widgets import DeviceActionWidget, ThermometerHelperWidget, CounterHelperWidget
from backend.models import Storage
from backend.models.Device import Device
from backend.models.Input import Input
from backend.models.Scenario import Scenario
from backend.models.Thermometer import Thermometer
from backend.models.Timer import Timer


class NoSettingsForm(forms.ModelForm):

    def __init__(self, plugin, *args, **kwargs):
        super(NoSettingsForm, self).__init__(*args, **kwargs)

    def clean_action_object(self):
        self.instance.action_object = self.cleaned_data['action_object']

    class Meta:
        model = LogicBlock
        exclude = ('active', 'inputs', 'outputs', '_data', 'content_type', 'object_id')
        widgets = {
            'x': forms.HiddenInput(),
            'y': forms.HiddenInput(),
            'program': forms.HiddenInput(),
            'type': forms.HiddenInput(),
            'function': forms.HiddenInput(),
        }


class InputDeviceStstusChangeForm(NoSettingsForm):
    action_object = forms.ModelChoiceField(Device.objects.all(), label=_('Device'))
    triggers = (
        (0, _('Any change')),
        (1, _('On/Off toggle')),
        (2, _('Off to On')),
        (3, _('On to Off')),
    )
    trigger = forms.ChoiceField(choices=triggers, widget=forms.RadioSelect())


class InputInputExecutedForm(NoSettingsForm):
    action_object = forms.ModelChoiceField(Input.objects.exclude(pk=1), label=_('Input'))


class InputScenarioExecutedForm(NoSettingsForm):
    action_object = forms.ModelChoiceField(Scenario.objects.all(), label=_('Scenario'))


class InputTemperatureChangedForm(NoSettingsForm):
    action_object = forms.ModelChoiceField(Thermometer.objects.all(), label=_('Thermometer'))

    def __init__(self, plugin, *args, **kwargs):
        super(InputTemperatureChangedForm, self).__init__(plugin, *args, **kwargs)
        self.plugin = plugin
        triggers = []
        for key, value in plugin.triggers.iteritems():
            triggers.append((key, force_unicode(value[0])))
        self.fields['trigger'] = forms.ChoiceField(choices=triggers, initial=0, widget=forms.RadioSelect())
        self.fields['temperature'] = forms.IntegerField(required=False)
        self.fields['start'] = forms.IntegerField(required=False)
        self.fields['end'] = forms.IntegerField(required=False)

        self.fields['helper'] = forms.NullBooleanField(required=False, widget=ThermometerHelperWidget())

    def clean_trigger(self):
        trigger = int(self.cleaned_data['trigger'])
        if trigger in self.plugin.triggers:
            self.instance.put_data('trigger', trigger)
            return trigger
        else:
            raise ValidationError(_('Trigger needs to be an available choice'))

    def clean_temperature(self):
        trigger = int(self.cleaned_data['trigger'])
        if trigger == 1 or trigger == 2:
            try:
                temperature = float(self.cleaned_data['temperature'])
                self.instance.put_data('temperature', temperature)

            except TypeError:
                raise ValidationError(_('Temperature needs to be a float'))

        return trigger

    def clean_start(self):
        trigger = int(self.cleaned_data['trigger'])
        if trigger == 3:
            try:
                start = float(self.cleaned_data['start'])
                self.instance.put_data('start', start)

            except TypeError:
                raise ValidationError(_('Start needs to be a float'))

        return trigger

    def clean_end(self):
        trigger = int(self.cleaned_data['trigger'])
        if trigger == 3:
            try:
                end = float(self.cleaned_data['end'])
                self.instance.put_data('end', end)

            except TypeError:
                raise ValidationError(_('End needs to be a float'))

        return trigger


class InputTimerExecutedForm(NoSettingsForm):
    action_object = forms.ModelChoiceField(Timer.objects.all(), label=_('Timer'))


class InputRSMemoryForm(NoSettingsForm):

    def __init__(self, plugin, *args, **kwargs):
        super(InputRSMemoryForm, self).__init__(plugin, *args, **kwargs)
        triggers = []
        for key, value in plugin.triggers.iteritems():
            triggers.append((key, force_unicode(value[0])))

        self.fields['memory'] = forms.CharField(max_length=50)
        self.fields['trigger'] = forms.ChoiceField(choices=triggers, initial=0, widget=forms.RadioSelect())

    def clean_memory(self):
        memory = self.cleaned_data['memory']
        self.instance.action_object = Storage.get_storage(memory, 'automation_rs_memory')
        return memory

    def clean_trigger(self):
        trigger = int(self.cleaned_data['trigger'])
        self.instance.put_data('trigger', trigger)
        return trigger


class InputCounterForm(NoSettingsForm):

    def __init__(self, plugin, *args, **kwargs):
        super(InputCounterForm, self).__init__(plugin, *args, **kwargs)
        triggers = []
        for key, value in plugin.triggers.iteritems():
            triggers.append((key, force_unicode(value[0])))

        self.fields['counter'] = forms.CharField(max_length=50)
        self.fields['trigger'] = forms.ChoiceField(choices=triggers, initial=0, widget=forms.RadioSelect())
        self.fields['value'] = forms.IntegerField(required=False)
        self.fields['start'] = forms.IntegerField(required=False)
        self.fields['end'] = forms.IntegerField(required=False)

        self.fields['helper'] = forms.NullBooleanField(required=False, widget=CounterHelperWidget())

    def clean_counter(self):
        counter = self.cleaned_data['counter']
        self.instance.action_object = Storage.get_storage(counter, 'automation_counter')
        return counter

    def clean_trigger(self):
        trigger = int(self.cleaned_data['trigger'])
        self.instance.put_data('trigger', trigger)
        return trigger

    def clean_value(self):
        trigger = int(self.cleaned_data['trigger'])
        if trigger in [0, 1, 2]:
            try:
                value = int(self.cleaned_data['value'])
                self.instance.put_data('value', value)

            except TypeError:
                raise ValidationError(_('Value needs to be a int'))

        return trigger

    def clean_start(self):
        trigger = int(self.cleaned_data['trigger'])
        if trigger == 3:
            try:
                start = int(self.cleaned_data['start'])
                self.instance.put_data('start', start)

            except TypeError:
                raise ValidationError(_('Start needs to be a int'))

        return trigger

    def clean_end(self):
        trigger = int(self.cleaned_data['trigger'])
        if trigger == 3:
            try:
                end = int(self.cleaned_data['end'])
                self.instance.put_data('end', end)

            except TypeError:
                raise ValidationError(_('End needs to be a int'))

        return trigger


class OutputDeviceStstusChangeForm(NoSettingsForm):
    action_object = forms.ModelChoiceField(Device.objects.all(), label=_('Device'))

    def __init__(self, *args, **kwargs):
        super(OutputDeviceStstusChangeForm, self).__init__(*args, **kwargs)
        self.fields['action'] = forms.CharField(max_length=9, widget=DeviceActionWidget(),
                                                initial=self.instance.get_data('action', 'off'))

    def clean_action(self):
        action = self.cleaned_data['action']
        self.instance.put_data('action', action)
        return action


class LogicDelayForm(NoSettingsForm):

    def __init__(self, plugin, *args, **kwargs):
        super(LogicDelayForm, self).__init__(plugin, *args, **kwargs)
        self.fields['seconds'] = forms.IntegerField()

    def clean_seconds(self):
        seconds = int(self.cleaned_data['seconds'])
        self.instance.put_data('seconds', seconds)
        return seconds


class OutputRSMemoryForm(NoSettingsForm):

    def __init__(self, plugin, *args, **kwargs):
        super(OutputRSMemoryForm, self).__init__(plugin, *args, **kwargs)
        actions = []
        for key, value in plugin.actions.iteritems():
            actions.append((key, force_unicode(value)))

        self.fields['memory'] = forms.CharField(max_length=50)
        self.fields['action'] = forms.ChoiceField(choices=actions, initial=0, widget=forms.RadioSelect())

    def clean_memory(self):
        memory = self.cleaned_data['memory']
        self.instance.action_object = Storage.get_storage(memory, 'automation_rs_memory')
        return memory

    def clean_action(self):
        action = int(self.cleaned_data['action'])
        self.instance.put_data('action', action)
        return action


class OutputCounterForm(NoSettingsForm):

    def __init__(self, plugin, *args, **kwargs):
        super(OutputCounterForm, self).__init__(plugin, *args, **kwargs)
        actions = []
        for key, value in plugin.actions.iteritems():
            actions.append((key, force_unicode(value)))

        self.fields['counter'] = forms.CharField(max_length=50)
        self.fields['action'] = forms.ChoiceField(choices=actions, initial=0, widget=forms.RadioSelect())
        self.fields['value'] = forms.IntegerField()

    def clean_counter(self):
        counter = self.cleaned_data['counter']
        self.instance.action_object = Storage.get_storage(counter, 'automation_counter')
        return counter

    def clean_action(self):
        action = int(self.cleaned_data['action'])
        self.instance.put_data('action', action)
        return action

    def clean_value(self):
        value = int(self.cleaned_data['value'])
        self.instance.put_data('value', value)
        return value