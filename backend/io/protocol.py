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
import os


def supported_types():
    dir = os.path.join(os.path.dirname(__file__), 'protocols')
    types = []
    for file in os.listdir(dir):
        if file.endswith('.py'):
            if file != '__init__.py':
                types.append((file[:-3], file[:-3]))

    return types


def get_class(protocol):
    tmpmodule = __import__('backend.io.protocols.%s' % protocol, fromlist=[protocol])
    tmpclass = getattr(tmpmodule, protocol)
    return tmpclass


class Protocol(object):
    CONNECTOR_TYPE = ''

    def __init__(self):
        self.SUPPORTED_ACTIONS = {
            "on": self.on,
            "off": self.off,
            "toggle": self.toggle,
        }

    def initialize(self, device):
        self.device = device

    def sync(self, *args, **kwargs):
        raise NotImplementedError

    def on(self, *args, **kwargs):
        raise NotImplementedError

    def off(self, *args, **kwargs):
        raise NotImplementedError

    def toggle(self, *args, **kwargs):
        if self.is_off:
            self.on()
        else:
            self.off()

    def new(self):
        pass

    def action(self, **kwargs):
        action = kwargs.get('action')
        if action is '':
            action = self.device.action
        try:
            self.SUPPORTED_ACTIONS[action](self, **kwargs)
        except IOError:
            return 'ConnectionError'

    @property
    def is_off(self):
        if self.device.status == 'off':
            return True
        else:
            return False


class DimLevelProtocol(Protocol):
    DIM_MIN = 0
    DIM_MAX = 1
    DIM_STEP = 1

    def action(self, **kwargs):
        action = kwargs.get('action')
        if action is '':
            action = self.device.action
        try:
            dim_level = int(action)
            action = 'dim_level'
            kwargs['dim_level'] = dim_level
        except ValueError:
            pass
        try:
            self.SUPPORTED_ACTIONS[action](self, **kwargs)
        except IOError:
            return 'ConnectionError'

    def getSteps(self):
        steps = []
        for step in range(self.DIM_MIN, self.DIM_MAX, self.DIM_STEP):
            steps.append(step)
        return steps