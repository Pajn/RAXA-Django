from django.db import models
from django.forms import ModelForm
from django.utils.translation import ugettext as _

class Floor(models.Model):
    name = models.CharField(_('Name'), max_length=30)

    def num_rooms(self):
        return self.room_set.all().__len__()
    num_rooms.short_description = _('Number of rooms')

    class Meta:
        app_label = 'backend'

    def __unicode__(self):
        return self.name

class FloorForm(ModelForm):
    class Meta:
        model = Floor

class Room(models.Model):
    name = models.CharField(_('Name'), max_length=30)
    floor = models.ForeignKey(Floor)

    class Meta:
        app_label = 'backend'

    def __unicode__(self):
        return self.name

class RoomForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['floor'].required = False
            self.fields['floor'].widget.attrs['disabled'] = 'disabled'

    def clean_floor(self):
        instance = getattr(self, 'instance', None)
        return instance.floor

    class Meta:
        model = Room