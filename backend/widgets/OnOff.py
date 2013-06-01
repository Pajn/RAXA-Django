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


class OnOff(Widget):
    def __init__(self, ui='default', *args, **kwargs):
        super(OnOff, self).__init__(*args, **kwargs)
        self.ui = ui

    def render(self, name, value, attrs=None):
        onselected = ''
        offselected = ''

        tpl = Template('''
                <input type="hidden" name="$name" id="$name$rand" value="$value" />
                <fieldset data-role="controlgroup" data-type="horizontal">
                    <input type="radio" name="$name$rand" id="$name$rand-1" $onselected />
                    <label for="$name$rand-1" onclick="$('#$name$rand').val('on')" class="on">$on</label>

                    <input type="radio" name="$name$rand" id="$name$rand-2" $offselected />
                    <label for="$name$rand-2" onclick="$('#$name$rand').val('off')" class="off">$off</label>
                </fieldset>''')

        SELECTED = 'checked="checked"'

        if value == 'on':
            onselected = SELECTED
        elif value == 'off':
            offselected = SELECTED

        return mark_safe(tpl.safe_substitute(name=name, value=value,
                                             rand=random.randint(0, 67234433),
                                             on=_('On'), off=_('Off'),
                                             onselected=onselected, offselected=offselected))