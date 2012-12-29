from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.forms import ModelForm, Form, CharField, HiddenInput
from django.utils.translation import ugettext as _
from backend.models.Device import Device
from backend.models.Scenario import Scenario
from backend.widgets.DeviceScenario import DeviceScenario, DeviceScenarioHidden
from backend.widgets import getWidget
from backend.widgets.Time import Time

class Timer(models.Model):
    name = models.CharField(_('Name'), max_length=30)
    time = models.TimeField(_('Time'))
    monday = models.BooleanField(_('Monday'))
    tuesday = models.BooleanField(_('Tuesday'))
    wednesday = models.BooleanField(_('Wednesday'))
    thursday = models.BooleanField(_('Thursday'))
    friday = models.BooleanField(_('Friday'))
    saturday = models.BooleanField(_('Saturday'))
    sunday = models.BooleanField(_('Sunday'))
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    action_object = generic.GenericForeignKey('content_type', 'object_id')
    action = models.CharField(_('Action'), max_length=9)

    class Meta:
        app_label = 'backend'

    def __unicode__(self):
        return self.name

    def execute(self):
        if isinstance(self.action_object, Device):
            self.action_object.object.action(action=self.action)
        elif isinstance(self.action_object, Scenario):
            self.action_object.execute()

    @staticmethod
    def get_timers_within(minutes):
        delta = timedelta(minutes=minutes)
        timestamp_from = datetime.now() - delta/2
        timestamp_to = datetime.now() + delta/2

        day_of_week = datetime.now().isoweekday()

        DAYS = {
            1: 'monday',
            2: 'tuesday',
            3: 'wednesday',
            4: 'thursday',
            5: 'friday',
            6: 'saturday',
            7: 'sunday',
        }

        kwargs = {
            'time__gte': timestamp_from.time(),
            'time__lt': timestamp_to.time(),
            DAYS[day_of_week]: True
        }

        return Timer.objects.filter(**kwargs)

class TimerForm(ModelForm):
    action_object = CharField(label='')
    device_scenario = CharField(widget=DeviceScenarioHidden(), required=False)
    content_type = CharField(widget=HiddenInput(), required=False)
    object_id = CharField(widget=HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(TimerForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        assert isinstance(instance, Timer)

        self.fields['action_object'].widget = DeviceScenario(value=instance.action_object)
        self.fields['action_object'].required = False
        self.fields['action_object'].widget.attrs['disabled'] = 'disabled'

        # Put action at the back
        action = self.fields.pop('action')
        self.fields.insert(len(self.fields), 'action', action)

        if isinstance(instance.action_object, Device):
            self.fields['action'].widget = getWidget(instance.action_object)
        else:
            self.fields['action'].required = False
            self.fields['action'].widget = HiddenInput()

    def clean_action_object(self):
        instance = getattr(self, 'instance', None)
        assert isinstance(instance, Timer)
        if instance and instance.action_object:
            return instance.action_object
        else:
            if 'device_scenario' in self.fields:
                return self._raw_value('device_scenario')
            else:
                raise ValidationError('Bad')

    def clean_content_type(self):
        instance = getattr(self, 'instance', None)
        assert isinstance(instance, Timer)
        if instance and instance.id:
            return instance.content_type
        else:
            if 'device_scenario' in self.fields:
                return ContentType.objects.get_for_model(type(self._raw_value('device_scenario')))
            else:
                raise ValidationError('Bad')

    def clean_object_id(self):
        instance = getattr(self, 'instance', None)
        assert isinstance(instance, Timer)
        if instance and instance.id:
            return instance.object_id
        else:
            if 'device_scenario' in self.fields:
                return self._raw_value('device_scenario').id
            else:
                raise ValidationError('Bad')

    class Meta:
        model = Timer
        exclude = ('content_type', 'object_id')
        widgets = {'time': Time()}

class TimerFormNew(Form):
    device_scenario = CharField(widget=DeviceScenario(), label=_('Device or scenario the timer to trigger'))