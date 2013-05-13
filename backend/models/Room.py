from django.core.exceptions import ValidationError
from xml.etree import ElementTree
from django.db import models
from django.forms import ModelForm
from django.forms.models import modelformset_factory
from django.utils.translation import ugettext_lazy as _


class Floor(models.Model):
    name = models.CharField(_('Name'), max_length=30)
    viewbox = models.CharField(_('Viewbox'), max_length=50)
    image = models.FileField(upload_to='floors')

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
        exclude = ('viewbox',)

    def clean_image(self):
        try:
            image = self.cleaned_data['image']
            svg = ElementTree.fromstring(''.join(image.readlines()))
            viewbox = svg.attrib['viewBox']
            try:
                if viewbox != '':
                    try:
                        if svg.attrib['width'] == '100%':
                            if svg.attrib['height'] == '100%':
                                self.instance.viewbox = viewbox
                                return image
                        #If the code reached this state either width or height check is false
                        raise ValidationError(_('A width and height of 100% is required'))
                    except KeyError:
                        raise ValidationError(_('A width and height of 100% is required'))
                else:
                    raise ValidationError(_('The viewBox attribute is required'))
            except KeyError:
                raise ValidationError(_('The viewBox attribute is required'))
        except Exception:
            raise ValidationError(_('An SVG image is required'))


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