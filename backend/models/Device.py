from django.db import models
from django.db.models.signals import post_init
from django.dispatch import receiver, Signal
from django.forms import ModelForm, HiddenInput
from django.utils.translation import ugettext_lazy as _

from . import Connector
from . import Room
from backend.io import protocol


device_status_change = Signal(providing_args=['device', 'status'])


class Device(models.Model):
    choices = protocol.supported_types()

    name = models.CharField(_('Name'), max_length=30)
    type = models.CharField(_('Type'), max_length=30, choices=choices)
    code = models.CharField(max_length=30)
    connector = models.ForeignKey(Connector, null=True, default=None)
    room = models.ForeignKey(Room)
    order = models.IntegerField(_('Order'), default=1)
    action = models.CharField(_('Action'), max_length=9)
    status = models.CharField(_('Status'), max_length=9, default='off')

    object = None

    class Meta:
        app_label = 'backend'

    def set_status(self, status):
        self.status = status
        self.save()
        device_status_change.send_robust(sender=self, device=self, status=status)

    def __unicode__(self):
        return self.name


class DeviceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        assert isinstance(instance, Device)

        if instance.object.CONNECTOR_TYPE is not None:
            if instance and instance.type:
                connector_type = protocol.get_class(instance.type)().CONNECTOR_TYPE
                self.fields['connector'].queryset = Connector.objects.filter(type=connector_type, usable=True)
        else:
            self.fields.pop('connector')

        if instance and instance.id:
            self.fields['type'].required = False
            self.fields['type'].widget.attrs['disabled'] = 'disabled'
        else:
            self.fields['code'].widget = HiddenInput()
            self.fields['action'].widget = HiddenInput()

    def clean_type(self):
        instance = getattr(self, 'instance', None)
        assert isinstance(instance, Device)

        if instance and instance.type:
            instance = getattr(self, 'instance', None)
            return instance.type
        else:
            return self.cleaned_data.get('type', None)

    class Meta:
        model = Device
        exclude = ('order', 'status')


class DeviceFormNew(ModelForm):
    class Meta:
        model = Device
        exclude = ('name', 'code', 'connector', 'room', 'order', 'action', 'status')


@receiver(post_init, sender=Device)
def initialize_device(instance=None, **kwargs):
    # This will load the correct protocol object to the model
    # instace is the model object
    assert isinstance(instance, Device)
    if instance and instance.type:
        # get the protocols class
        instance.object = protocol.get_class(instance.type)()
        # initialize the object
        instance.object.initialize(instance)