from django.db import models
from django.db.models.signals import post_init
from django.dispatch import receiver
from django.forms import ModelForm
from django.utils.translation import ugettext as _

class Connector(models.Model):
    name = models.CharField(_('Name'), max_length=30)
    type = models.CharField(_('Type'), max_length=30)
    code = models.CharField(_('Code'), max_length=30)

    class Meta:
        app_label = 'backend'

    def __unicode__(self):
        return self.name

class ConnectorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConnectorForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['type'].required = False
            self.fields['type'].widget.attrs['disabled'] = 'disabled'
            self.fields['code'].required = False
            self.fields['code'].widget.attrs['disabled'] = 'disabled'

    def clean_type(self):
        instance = getattr(self, 'instance', None)
        return instance.type

    def clean_code(self):
        instance = getattr(self, 'instance', None)
        return instance.code

    class Meta:
        model = Connector

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