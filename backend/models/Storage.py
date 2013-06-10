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
import json
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Storage(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    owner = models.CharField(_('Owner'), max_length=50)

    _data = models.TextField(_('Data'), default='{}')

    class Meta:
        app_label = 'backend'

    @property
    def data(self):
        return json.loads(self._data)

    @data.setter
    def data(self, data):
        self._data = json.dumps(data)

    def put_data(self, key, value, commit=True):
        data = self.data
        data[key] = value
        self.data = data
        if commit:
            self.save()

    def get_data(self, key, default):
        data = self.data
        try:
            return data[key]
        except KeyError:
            return default

    @classmethod
    def get_storage(cls, name, owner):
        try:
            storage = cls.objects.get(name=name, owner=owner)
        except cls.DoesNotExist:
            storage = cls()
            storage.name = name
            storage.owner = owner
            storage.save()
        return storage
