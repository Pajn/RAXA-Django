from django.db import models
from django.db.models.signals import post_init
from django.dispatch import receiver
from . import Connector
from . import Room

class Device(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    code = models.CharField(max_length=30)
    connector = models.ForeignKey(Connector)
    room = models.ForeignKey(Room)
    order = models.IntegerField()
    action = models.CharField(max_length=8)

    class Meta:
        app_label = 'backend'

    def __unicode__(self):
        return self.name

@receiver(post_init, sender=Device)
def initialize_device(**kwargs):
    # This will load the correct protocol object to the model
    # instace is the model object
    instance = kwargs.get('instance')
    # import the protocols module
    tmpmodule = __import__("backend.out.protocols." + instance.type, fromlist=[instance.type])
    # get the protocols class
    tmpclass = getattr(tmpmodule, instance.type)
    # create the protocol object
    instance.object = tmpclass()
    # initialize the object
    instance.object.initialize(instance)