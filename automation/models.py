import json
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from automation import logic_helpers
from automation.plugin_mounts import InputBlockFunction, LogicBlockFunction, OutputBlockFunction


class Program(models.Model):
    name = models.CharField(_('Name'), max_length=30)
    active = models.BooleanField(_('Active'), default=True)


class LogicBlock(models.Model):
    program = models.ForeignKey(Program)
    type = models.IntegerField(_('Type'))
    function = models.CharField(_('Function'), max_length=50)
    active = models.BooleanField(_('Active'), default=False)

    x = models.PositiveIntegerField()
    y = models.PositiveIntegerField()

    _data = models.TextField(_('Data'), default='{}')

    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    action_object = generic.GenericForeignKey('content_type', 'object_id')

    @property
    def data(self):
        print self._data
        return json.loads(self._data)

    @data.setter
    def data(self, data):
        self._data = json.dumps(data)

    def put_data(self, key, value):
        data = self.data
        data[key] = value
        self.data = data

    def get_data(self, key, default):
        data = self.data
        try:
            return data[key]
        except KeyError:
            return default

    @property
    def plugin(self):
        if self.type == logic_helpers.LogicBlockTypes.input:
            return InputBlockFunction.get_plugin(self.function)
        elif self.type == logic_helpers.LogicBlockTypes.gate:
            return LogicBlockFunction.get_plugin(self.function)
        elif self.type == logic_helpers.LogicBlockTypes.output:
            return OutputBlockFunction.get_plugin(self.function)

    _label = None

    @property
    def label(self):
        if self._label is None:
            self._label = self.plugin.get_label(self).split('\n')
        return self._label


class Link(models.Model):
    start = models.ForeignKey(LogicBlock, related_name='outputs')
    end = models.ForeignKey(LogicBlock, related_name='inputs')

    @property
    def start_x(self):
        if self.start.type == logic_helpers.LogicBlockTypes.input:
            return self.start.x + 65
        elif self.start.type == logic_helpers.LogicBlockTypes.gate:
            return self.start.x + 30

    @property
    def start_y(self):
        if self.start.type == logic_helpers.LogicBlockTypes.input:
            return self.start.y + 80
        elif self.start.type == logic_helpers.LogicBlockTypes.gate:
            return self.start.y + 60

    @property
    def end_x(self):
        if self.end.type == logic_helpers.LogicBlockTypes.gate:
            return self.end.x + 30 - self.start_x
        elif self.end.type == logic_helpers.LogicBlockTypes.output:
            return self.end.x + 65 - self.start_x

    @property
    def end_y(self):
        return self.end.y + 15 - self.start_y

    @property
    def end_y_50(self):
        return self.end_y - 50