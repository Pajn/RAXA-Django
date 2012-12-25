from django.db import models
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from . import Device

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
                scenario_device.device.object.action(scenario_device.action)
        else:
            for scenario_device in self.scenariodevice_set.all():
                scenario_device.device.object.action(action)

class ScenarioDevice(models.Model):
    device = models.ForeignKey(Device)
    scenario = models.ForeignKey(Scenario)
    action = models.CharField(max_length=8)

    class Meta:
        app_label = 'backend'

class ScenarioForm(ModelForm):
    class Meta:
        model = Scenario
        exclude = ('order',)