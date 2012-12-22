from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Timer(models.Model):
    name = models.CharField(max_length=30)
    #days = models.
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    action_object = generic.GenericForeignKey('content_type', 'object_id')
    action = models.CharField(max_length=8)

    class Meta:
        app_label = 'backend'