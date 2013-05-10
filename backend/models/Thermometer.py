from django.db import models
from django.db.models.signals import post_init
from django.dispatch import receiver, Signal
from django.forms import ModelForm
from django.forms.models import modelformset_factory
from django.utils.translation import ugettext_lazy as _
from backend.io.thermometer import get_class


temperature_changed = Signal(providing_args=['thermometer', 'temperature'])


class Thermometer(models.Model):
    name = models.CharField(_('Name'), max_length=30)
    type = models.CharField(_('Type'), max_length=30)
    code = models.CharField(_('Code'), max_length=30)
    temperature = models.FloatField(_('Temperature'))

    object = None

    class Meta:
        app_label = 'backend'

    def __unicode__(self):
        return self.name

    def set_temp(self, temp):
        self.temperature = temp
        self.save()
        temperature_changed.send(sender=self, thermometer=self, temperature=temp)

    def get_temp(self):
        return round(self.temperature, 1)


thermometer_form_set = None


def ThermometerFormSet(*args, **kwargs):
    global thermometer_form_set

    if thermometer_form_set is None:
        thermometer_form_set = modelformset_factory(Thermometer, form=ThermometerForm, can_delete=True, extra=0)

    return thermometer_form_set(*args, **kwargs)


class ThermometerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ThermometerForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['type'].required = False
            self.fields['type'].widget.attrs['disabled'] = 'disabled'
            self.fields['code'].required = False
            self.fields['code'].widget.attrs['disabled'] = 'disabled'
            self.fields['temperature'].required = False
            self.fields['temperature'].widget.attrs['disabled'] = 'disabled'

    def clean_type(self):
        instance = getattr(self, 'instance', None)
        return instance.type

    def clean_code(self):
        instance = getattr(self, 'instance', None)
        return instance.code

    def clean_temperature(self):
        instance = getattr(self, 'instance', None)
        return instance.temperature

    class Meta:
        model = Thermometer


@receiver(post_init, sender=Thermometer)
def initialize_thermometer(**kwargs):
    # This will load the correct thermometer object to the model
    #instace is the model object
    instance = kwargs.get('instance')
    #create the thermometer object
    instance.object = get_class(instance.type)()
    #initialize the object
    instance.object.initialize(instance)