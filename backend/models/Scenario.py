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
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.dispatch import Signal
from django.forms import ModelForm, ModelChoiceField, Form, HiddenInput
from django.forms.models import modelformset_factory
from django.utils.translation import ugettext_lazy as _
from django.db import transaction

from . import Device
from backend.widgets import getWidget


scenario_executing = Signal(providing_args=['scenario'])
scenario_executed = Signal(providing_args=['scenario'])


class Scenario(models.Model):
    name = models.CharField(_('Name'), max_length=30)
    is_hidden = models.BooleanField(_('Is hidden'))
    order = models.IntegerField(_('Order'), default=1)

    class Meta:
        app_label = 'backend'

    def __unicode__(self):
        return self.name

    def execute(self, action=None):
        scenario_executing.send(sender=self, scenario=self)

        transaction.enter_transaction_management()
        transaction.managed(True)

        errors = {}

        if action is None:
            for scenario_device in self.scenariodevice_set.all().select_related('device'):
                errors[scenario_device] = scenario_device.device.object.action(action=scenario_device.action)
        else:
            for scenario_device in self.scenariodevice_set.all().select_related('device'):
                errors[scenario_device] = scenario_device.device.object.action(action=action)

        transaction.commit()

        transaction.leave_transaction_management()

        scenario_executed.send(sender=self, scenario=self, errors=errors)

        return errors


scenario_form_set = None


def ScenarioFormSet(*args, **kwargs):
    global scenario_form_set

    if scenario_form_set is None:
        scenario_form_set = modelformset_factory(Scenario, exclude=('order',), can_delete=True)
    return scenario_form_set(*args, **kwargs)


class ScenarioForm(ModelForm):
    class Meta:
        model = Scenario
        exclude = ('order',)


class ScenarioDevice(models.Model):
    device = models.ForeignKey(Device)
    scenario = models.ForeignKey(Scenario)
    action = models.CharField(_('Action'), max_length=9)

    class Meta:
        app_label = 'backend'


scenario_device_form_set = None


def ScenarioDeviceFormSet(*args, **kwargs):
    global scenario_device_form_set

    if scenario_device_form_set is None:
        scenario_device_form_set = modelformset_factory(ScenarioDevice, exclude=('scenario',), can_delete=True)
    formset = scenario_device_form_set(*args, **kwargs)
    for form in formset:
        if 'device' in form.initial:
            print form.initial['device']
            form.fields['action'].widget = getWidget(form.instance.device)
    return formset


class ScenarioDeviceForm(ModelForm):
    device_new = ModelChoiceField(widget=HiddenInput(), queryset=Device.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(ScenarioDeviceForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        self.fields['device'].required = False
        self.fields['device'].widget.attrs['disabled'] = 'disabled'

        if instance is not None:
            try:
                self.fields['action'].widget = getWidget(instance.device)
            except ObjectDoesNotExist:
                pass

    def clean_device(self):
        instance = getattr(self, 'instance', None)
        if instance.device.id != 0:
            return instance.device
        else:
            if 'device_new' in self.fields:
                return self.cleaned_data.get('device_new', None)
            else:
                return self.cleaned_data.get('device', None)

    class Meta:
        model = ScenarioDevice
        exclude = ('scenario',)


class ScenarioDeviceFormAction(ModelForm):
    device_new = ModelChoiceField(widget=HiddenInput(), queryset=Device.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(ScenarioDeviceFormAction, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance is not None:
            try:
                self.fields['action'].widget = getWidget(instance.device)
            except ObjectDoesNotExist:
                pass

    class Meta:
        model = ScenarioDevice
        exclude = ('scenario', 'device')


class ScenarioDeviceFormNew(Form):
    device = ModelChoiceField(label=_('Device'), queryset=Device.objects.all())

    def __init__(self, *args, **kwargs):
        super(ScenarioDeviceFormNew, self).__init__(*args, **kwargs)