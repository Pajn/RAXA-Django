from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=30)
    floor = models.IntegerField()

    class Meta:
        app_label = 'backend'

    def __unicode__(self):
        return self.name