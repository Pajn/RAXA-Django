from django.db import models
from django.forms import ModelForm
from django.forms.models import modelformset_factory
from django.utils.translation import ugettext_lazy as _


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


floor_form_set = None


def FloorFormSet(*args, **kwargs):
    global floor_form_set

    if floor_form_set is None:
        floor_form_set = modelformset_factory(Floor, form=FloorForm, can_delete=True)

    return floor_form_set(*args, **kwargs)


class Room(models.Model):
    name = models.CharField(_('Name'), max_length=30)
    floor = models.ForeignKey(Floor)

    class Meta:
        app_label = 'backend'

    def __unicode__(self):
        return '%s - %s' % (self.name, self.floor.name)


class RoomForm(ModelForm):
    class Meta:
        model = Room


room_form_set = None


def RoomFormSet(*args, **kwargs):
    global room_form_set

    if room_form_set is None:
        room_form_set = modelformset_factory(Room, form=RoomForm, can_delete=True)

    return room_form_set(*args, **kwargs)