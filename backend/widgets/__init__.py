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
from OnOff import OnOff
from OnOffDimLevel import OnOffDimLevel
from OnOffColorWheel import OnOffColorWheel


def getWidget(device, ui='default'):
    if 'color_wheel' in device.object.SUPPORTED_ACTIONS:
        return OnOffColorWheel(ui=ui, device=device)
    elif 'dim_level' in device.object.SUPPORTED_ACTIONS:
        return OnOffDimLevel(ui=ui, device=device)
    else:
        return OnOff(ui=ui)