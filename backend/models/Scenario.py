from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.forms import ModelForm, ModelChoiceField, Form, HiddenInput
from django.utils.translation import ugettext as _
from . import Device
from backend.widgets import getWidget

class Scenario(models.Model):
    name = models.CharField(_('Name'), max_length=30)
    is_hidden = models.BooleanField(_('Is hidden'))
    order = models.IntegerField(_('Order'), default=1)

    class Meta:
        app_label = 'backend'

    def __unicode__(self):
        return self.name

    def execute(self, action=''):
        if action is not '':
            for scenario_device in self.scenariodevice_set.all():
                scenario_device.device.object.action(action=scenario_device.action)
        else:
            for scenario_device in self.scenariodevice_set.all():
                scenario_device.device.object.action(action=action)

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

class ScenarioDeviceFormNew(Form):
    device = ModelChoiceField(label=_('Device'), queryset=Device.objects.all())
    def __init__(self, *args, **kwargs):
        super(ScenarioDeviceFormNew, self).__init__(*args, **kwargs)