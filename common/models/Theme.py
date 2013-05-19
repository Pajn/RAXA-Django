from django.db.models.signals import post_delete
from string import Template
from django.dispatch import receiver
from django.forms.widgets import Widget
from django.core.exceptions import ValidationError
from django.db import models
from django import forms
from django.forms.models import ModelForm, modelformset_factory, BaseModelFormSet
from django.forms.formsets import DELETION_FIELD_NAME
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


class EmptyHiddenFile(Widget):
    def render(self, name, value, attrs=None):
        tpl = Template('''<input type="file" name="$name" style="display: none;"></input>''')

        return mark_safe(tpl.safe_substitute(name=name))


class ActiveTheme(Widget):
    def render(self, name, value, attrs=None):
        if self.value != 0:
            tpl = Template('''<input type="radio" value="$value" name="theme"$selected></input>''')

            if self.selected:
                selected = ' checked="checked"'
            else:
                selected = ''

            return mark_safe(tpl.safe_substitute(value=self.value, selected=selected))
        else:
            return mark_safe('')


class Theme(models.Model):
    name = models.CharField(_('Name'), max_length=30)
    builtin = models.BooleanField(default=False)
    css = models.FileField(_('CSS'), upload_to='themes')

    class Meta:
        app_label = 'common'

    def __unicode__(self):
        return self.name


@receiver(post_delete, sender=Theme)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    if instance.css != '':
        instance.css.delete(False)


def ThemeFormSet(active, *args, **kwargs):

    class ThemeForm(ModelForm):
        active = forms.IntegerField(label=_('Active'), required=False, widget=ActiveTheme())

        def __init__(self, *args, **kwargs):
            super(ThemeForm, self).__init__(*args, **kwargs)

            if self.instance and self.instance.css:
                self.fields['css'].widget = EmptyHiddenFile()
                self.fields['active'].widget.value = self.instance.id
                self.fields['active'].widget.selected = active == self.instance.id
            else:
                self.fields['active'].widget.value = 0

        def clean_css(self):
            image = self.cleaned_data['css']
            if image.__str__().endswith('.css'):
                return self.cleaned_data['css']
            else:
                raise ValidationError(_('A CSS file is required'))

        class Meta:
            model = Theme
            fields = ('active', 'name', 'css')

    theme_form_set = modelformset_factory(Theme, form=ThemeForm, can_delete=True, formset=ThemeModelFormSet)

    return theme_form_set(*args, **kwargs)


class ThemeModelFormSet(BaseModelFormSet):
    def add_fields(self, form, index):
        super(ThemeModelFormSet, self).add_fields(form, index)

        if self.can_delete and form.instance.builtin:
            form.fields.pop(DELETION_FIELD_NAME)