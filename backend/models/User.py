'''
Copyright (C) 2013 Rasmus Eneman <rasmus@eneman.eu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from django.forms.fields import CharField, ChoiceField
from django.forms.widgets import PasswordInput, RadioSelect
from django.forms.forms import Form
from django.db import models
from django.utils.crypto import salted_hmac
from django.utils.translation import ugettext_lazy as _
from common.models.Theme import Theme


class User(models.Model):
    username = models.CharField(_('Username'), max_length=40, unique=True, db_index=True)
    password = models.CharField(_('Password'), max_length=128)
    api_key = models.CharField(_('Api key'), max_length=40, unique=True, db_index=True)
    allow_local = models.BooleanField(_('Allow local'), default=True)
    is_active = models.BooleanField(default=False)
    theme = models.ForeignKey(Theme, default=1)

    class Meta:
        app_label = 'backend'

    def check_password(self, password):
        print 'Set: ' + self.password
        print 'Check: ' + salted_hmac(self.username, password).hexdigest()
        return salted_hmac(self.username, password).hexdigest() == self.password

    def set_password(self, password):
        self.password = salted_hmac(self.username, password).hexdigest()
        self.save()


class LoginForm(Form):
    password = CharField(widget=PasswordInput())


class SecurityForm(ModelForm):
    password1 = CharField(widget=PasswordInput(), required=False)
    password2 = CharField(widget=PasswordInput(), required=False)

    def clean_password2(self):
        instance = getattr(self, 'instance', None)
        assert isinstance(instance, User)

        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            raise ValidationError(_("Passwords doesn't match"))
        else:
            return password2

    class Meta:
        model = User
        exclude = ('api_key', 'username', 'password')


class ThemeForm(ModelForm):
    class Meta:
        model = User
        fields = ('theme',)
        widgets = {
            'theme': RadioSelect()
        }