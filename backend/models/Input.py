import time
import pytz

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.dispatch import Signal
from django.forms import ModelForm, Form, CharField, HiddenInput
from django.utils.translation import ugettext_lazy as _

import datetime
from backend.models.Device import Device
from backend.models.Scenario import Scenario
from backend.widgets.DeviceScenario import DeviceScenario, DeviceScenarioHidden
from backend.widgets.Time import Time
from backend.widgets import getWidget


input_received = Signal(providing_args=['protocol', 'data'])
input_executed = Signal(providing_args=['input'])


class Input(models.Model):
    name = models.CharField(_('Name'), max_length=30)
    protocol = models.CharField(_('Protocol'), max_length=30)
    data = models.CharField(_('Data'), max_length=30)
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    action_object = generic.GenericForeignKey('content_type', 'object_id')
    action = models.CharField(_('Action'), max_length=9)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'backend'

    def execute(self):
        timedelta = datetime.datetime.now(pytz.utc) - self.timestamp
        if timedelta.total_seconds() > 2:
            if isinstance(self.action_object, Device):
                self.action_object.object.action(action=self.action)
            elif isinstance(self.action_object, Scenario):
                self.action_object.execute()

            input_executed.send(sender=self, input=object)

    @staticmethod
    def received(protocol, data):
        input_received.send(sender=None, protocol=protocol, data=data)
        try:
            object = Input.objects.exclude(pk=1).get(protocol=protocol, data=data)
            object.execute()
        except Input.DoesNotExist:
            try:
                object = Input.objects.get(pk=1)
            except Input.DoesNotExist:
                object = Input(pk=1)
            object.name = 'found'
            object.protocol = protocol
            object.data = data
            object.save()


    @staticmethod
    def scan(timeout=10):
        try:
            input = Input.objects.get(pk=1)
        except Input.DoesNotExist:
            input = Input(pk=1)
        input.name = 'scanning'
        input.protocol = ''
        input.data = ''
        input.content_type_id = None
        input.object_id = None
        input.action = ''
        input.save()

        found = False
        timedout = False

        start_time = time.time()

        while not found and not timedout:
            try:
                input = Input.objects.get(pk=1, name='found')
                found = True
            except Input.DoesNotExist:
                current_time = time.time() - start_time
                if current_time >= timeout:
                    timedout = True
                time.sleep(0.5)

        if found:
            return input
        else:
            return None


class InputForm(ModelForm):
    action_object = CharField(label='')
    device_scenario = CharField(widget=DeviceScenarioHidden(), required=False)
    content_type = CharField(widget=HiddenInput(), required=False)
    object_id = CharField(widget=HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(InputForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        assert isinstance(instance, Input)

        self.fields['action_object'].widget = DeviceScenario(value=instance.action_object)
        if instance and instance.action_object:
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
        assert isinstance(instance, Input)
        if instance and instance.action_object:
            return instance.action_object
        else:
            if 'device_scenario' in self.fields:
                instance.action_object = self._raw_value('device_scenario')
                instance.action = 'off'
                return self._raw_value('device_scenario')
            else:
                raise ValidationError('Bad')

    def clean_content_type(self):
        instance = getattr(self, 'instance', None)
        assert isinstance(instance, Input)
        if instance and instance.id:
            return instance.content_type
        else:
            if 'device_scenario' in self.fields:
                return ContentType.objects.get_for_model(type(self._raw_value('device_scenario')))
            else:
                raise ValidationError('Bad')

    def clean_object_id(self):
        instance = getattr(self, 'instance', None)
        assert isinstance(instance, Input)
        if instance and instance.id:
            return instance.object_id
        else:
            if 'device_scenario' in self.fields:
                return self._raw_value('device_scenario').id
            else:
                raise ValidationError('Bad')

    class Meta:
        model = Input
        exclude = ('content_type', 'object_id', 'timestamp')
        widgets = {'time': Time()}


class InputFormNew(Form):
    device_scenario = CharField(widget=DeviceScenario(), label=_('Device or scenario for the input to trigger'))