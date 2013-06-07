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
from backend.plugin_helpers import PluginMount


class InputBlockFunction:
    """
    Mount point for plugins which need to registrar an input block function

    Plugins implementing this reference should provide the following attributes:

    label       The label of the button

    Plugins implementing this reference may provide the following attributes:

    settings_view A class based generic_view which provides settings form, an id to a LogicBlock
                  model will be provides as a GET variable if applicable

    Plugins implementing this reference should provide the following methods:

    get_label(model)
        model LogicBlock the model the block should represent
        returns tuple with up to three string for each row
    """
    __metaclass__ = PluginMount


class LogicBlockFunction:
    """
    Mount point for plugins which need to registrar an input block function

    Plugins implementing this reference should provide the following attributes:

    label       The label of the button

    Plugins implementing this reference may provide the following attributes:

    settings_view A class based generic_view which provides settings form, an id to a LogicBlock
                  model will be provides as a GET variable if applicable

    Plugins implementing this reference should provide the following methods:

    get_label(model)
        model LogicBlock the model the block should represent
        returns string the label. Split up to three lines using ;

    check_logic(inputs)
        attribute inputs list<boolean> a list of the active state of all inputs
        returns boolean a boolean of the active state based on the state of the inputs
    """
    __metaclass__ = PluginMount


class OutputBlockFunction:
    """
    Mount point for plugins which need to registrar an input block function

    Plugins implementing this reference should provide the following attributes:

    label       The label of the button

    Plugins implementing this reference may provide the following attributes:

    settings_view A class based generic_view which provides settings form, an id to a LogicBlock
                  model will be provides as a GET variable if applicable

    Plugins implementing this reference should provide the following methods:

    get_label(model)
        model LogicBlock the model the block should represent
        returns string the label. Split up to three lines using ;
    """
    __metaclass__ = PluginMount