from django.db import models
from django.db.models.signals import post_init
from django.dispatch import receiver
from . import Connector
from . import Room
from django.forms import ModelForm
from django.utils.translation import ugettext as _
import os

def supported_types():
    types = []
    for n in os.listdir('backend/out/protocols'):
        if n.endswith('.py'):
            if n != 'Protocol.py' and n != '__init__.py':
                types.append((n[:-3], n[:-3]))
    return types

class Device(models.Model):
    choices = supported_types()

    name = models.CharField(_('Name'), max_length=30)
    type = models.CharField(_('Type'), max_length=30, choices=choices)
    code = models.CharField(max_length=30)
    connector = models.ForeignKey(Connector)
    room = models.ForeignKey(Room)
    order = models.IntegerField(_('Order'), )
    action = models.CharField(_('Action'), max_length=8)

    object = None

    class Meta:
        app_label = 'backend'


    def __unicode__(self):
        return self.name

class DeviceFormOld(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeviceFormOld, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        assert isinstance(instance, Device)

        self.fields['type'].required = False
        self.fields['type'].widget.attrs['disabled'] = 'disabled'

    def clean_type(self):
        instance = getattr(self, 'instance', None)
        return instance.type

    class Meta:
        model = Device
        exclude = ('order',)

class DeviceFormNew(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeviceFormNew, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        assert isinstance(instance, Device)

            #self.fields['type'].widget = widgets.Select()
            #self.fields['action'].widget = instance.object.WIDGET

    class Meta:
        model = Device
        exclude = ('order',)

class a:
    pass


@receiver(post_init, sender=Device)
def initialize_device(instance=None, **kwargs):
    # This will load the correct protocol object to the model
    # instace is the model object
    assert isinstance(instance, Device)
    if instance and instance.type:
        # import the protocols module
        tmpmodule = __import__('backend.out.protocols.%s' % instance.type, fromlist=[instance.type])
        # get the protocols class
        tmpclass = getattr(tmpmodule, instance.type)
        # create the protocol object
        instance.object = tmpclass()
        # initialize the object
        instance.object.initialize(instance)