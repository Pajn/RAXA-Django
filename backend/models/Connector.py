from django.db import models
from django.db.models.signals import post_init
from django.dispatch import receiver
from django.forms import ModelForm
from django.forms.models import modelformset_factory
from django.utils.translation import ugettext_lazy as _
from backend.io.connector import supported_types, get_class


class Connector(models.Model):
    name = models.CharField(_('Name'), max_length=30)
    type = models.CharField(_('Type'), max_length=30)
    code = models.CharField(_('Code'), max_length=30)
    version = models.CharField(_('Version'), max_length=30)
    usable = models.BooleanField(_('Usable'))

    object = None

    class Meta:
        app_label = 'backend'

    def __unicode__(self):
        return self.name

    @staticmethod
    def scan(timeout=10):
        for type in supported_types():
            pass


def ConnectorFormSet(*args, **kwargs):
    formset = modelformset_factory(Connector, form=ConnectorForm, can_delete=True, extra=0)
    return formset(*args, **kwargs)


class ConnectorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConnectorForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['type'].required = False
            self.fields['type'].widget.attrs['disabled'] = 'disabled'
            self.fields['type'].widget.attrs['size'] = '10'
            self.fields['code'].required = False
            self.fields['code'].widget.attrs['disabled'] = 'disabled'
            self.fields['code'].widget.attrs['size'] = '10'
            self.fields['version'].required = False
            self.fields['version'].widget.attrs['disabled'] = 'disabled'
            self.fields['version'].widget.attrs['size'] = '10'

    def clean_type(self):
        instance = getattr(self, 'instance', None)
        return instance.type

    def clean_code(self):
        instance = getattr(self, 'instance', None)
        return instance.code

    def clean_version(self):
        instance = getattr(self, 'instance', None)
        return instance.version

    class Meta:
        model = Connector
        exclude = ('usable',)


@receiver(post_init, sender=Connector)
def initialize_connector(**kwargs):
    # This Will load the correct connector object to the model
    #instace is the model object
    instance = kwargs.get('instance')
    #create the connector object
    instance.object = get_class(instance.type)()
    #initialize the object
    instance.object.initialize(instance)