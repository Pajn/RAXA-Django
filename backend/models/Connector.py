from django.db import models
from django.db.models.signals import post_init
from django.dispatch import receiver

class Connector(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    code = models.CharField(max_length=30)

    class Meta:
        app_label = 'backend'

    def __unicode__(self):
        return self.name

@receiver(post_init, sender=Connector)
def initialize_connector(**kwargs):
    # This Will load the correct connector object to the model
    #instace is the model object
    instance = kwargs.get('instance')
    #import the connector module
    tmpmodule = __import__("backend.out.connectors." + instance.type, fromlist=[instance.type])
    #get the connector class
    tmpclass = getattr(tmpmodule, instance.type)
    #create the connector object
    instance.object = tmpclass()
    #initialize the object
    instance.object.initialize(instance)