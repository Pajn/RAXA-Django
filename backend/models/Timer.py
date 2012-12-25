from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.forms import ModelForm
from django.utils.translation import ugettext as _

class Timer(models.Model):
    name = models.CharField(_('Name'), max_length=30)
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
    action = models.CharField(_('Action'), max_length=8)

    class Meta:
        app_label = 'backend'

class TimerForm(ModelForm):
    class Meta:
        model = Timer