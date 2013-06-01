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
from __future__ import unicode_literals
import random
from string import Template

from django.forms import Widget
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


class OnOffDimLevel(Widget):
    def __init__(self, ui='default', device=None, *args, **kwargs):
        super(OnOffDimLevel, self).__init__(*args, **kwargs)
        self.ui = ui
        self.device = device

    def render(self, name, value, attrs=None):
        onselected = ''
        offselected = ''
        dimselected = ''
        dimhide = 'none'
        dimvalue = self.device.action
        dimmin = self.device.object.DIM_MIN
        dimmax = self.device.object.DIM_MAX
        dimstep = self.device.object.DIM_STEP

        tpl = Template('''
                <input type="hidden" name="$name" id="$name$rand" value="$value" />
                <fieldset data-role="controlgroup" data-type="horizontal">
                    <input type="radio" name="$name$rand" id="$name$rand-1" $onselected />
                    <label for="$name$rand-1" onclick="$('#$name$rand').val('on');$('#$name$rand-sliderdiv').hide()" class="on">$on</label>

                    <input type="radio" name="$name$rand" id="$name$rand-2" $offselected />
                    <label for="$name$rand-2" onclick="$('#$name$rand').val('off');$('#$name$rand-sliderdiv').hide()" class="off">$off</label>

                    <input type="radio" name="$name$rand" id="$name$rand-3" $dimselected />
                    <label for="$name$rand-3" onclick="$('#$name$rand').val($('#$name$rand-slider').val());$('#$name$rand-sliderdiv').show()" class="dim">$dim</label>
                </fieldset>
                <div id="$name$rand-sliderdiv" style="display: $dimhide;">
                    <input type="range" id="$name$rand-slider" onchange="$('#$name$rand').val($(this).val())" value="$dimvalue" min="$dimmin" max="$dimmax" step="$dimstep" />
                    <label for="$name$rand-slider" class="ui-hidden-accessible">$dim_value</label>
                </div>''')

        SELECTED = 'checked="checked"'

        if value == 'on':
            onselected = SELECTED
        elif value == 'off':
            offselected = SELECTED
        elif value.isdigit():
            dimselected = SELECTED
            dimvalue = value
            dimhide = 'block'

        return mark_safe(tpl.safe_substitute(name=name, value=value,
                                             rand=random.randint(0, 67234433),
                                             on=_('On'), off=_('Off'), dim=_('Dim'), dim_value=_('Dim Value'),
                                             onselected=onselected, offselected=offselected, dimselected=dimselected,
                                             dimhide=dimhide, dimvalue=dimvalue, dimmin=dimmin, dimmax=dimmax,
                                             dimstep=dimstep
        ))