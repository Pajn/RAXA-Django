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


class OnOffColorWheel(Widget):
    def __init__(self, ui='default', device=None, *args, **kwargs):
        super(OnOffColorWheel, self).__init__(*args, **kwargs)
        self.ui = ui
        self.device = device

    def render(self, name, value, attrs=None):
        onselected = ''
        offselected = ''
        cwselected = ''
        cwhide = 'none'

        tpl = Template('''
                <input type="hidden" name="$name" id="$name$rand" value="$value" />
                <fieldset data-role="controlgroup" data-type="horizontal">
                    <input type="radio" name="$name$rand" id="$name$rand-1" $onselected />
                    <label for="$name$rand-1" onclick="$('#$name$rand').val('on');$('#$name$rand-sliderdiv').hide()" class="on">$on</label>

                    <input type="radio" name="$name$rand" id="$name$rand-2" $offselected />
                    <label for="$name$rand-2" onclick="$('#$name$rand').val('off');$('#$name$rand-sliderdiv').hide()" class="off">$off</label>

                    <input type="radio" name="$name$rand" id="$name$rand-3" $cwselected />
                    <label for="$name$rand-3" onclick="$('#$name$rand').val($('#$name$rand-slider').val());$('#$name$rand-sliderdiv').show()" class="color">$color</label>
                </fieldset>
                <div id="$name$rand-sliderdiv" style="position: relative; width: 200px; height: 200px; display: $cwhide;">
                    <img src="/static/images/color_wheel.png"
                         style="position: absolute; top: 0px; left: 0px; width: 200px; height: 200px;"
                         onload="$(this).click(function(e) {
                             var offset = $(this).offset();
                             var x = e.clientX - offset.left;
                             var y = e.clientY - offset.top;
                             var x_diff = x - 100;
                             var y_diff = y - 100;
                             var angle = (180 * Math.atan(x_diff/y_diff)) / Math.PI;
                             if (y_diff < 0) { angle += 180; }
                             else if (x_diff < 0 && y_diff > 0) { angle += 360; }
                             var angle = Math.floor(angle);
                             $('#$name$rand').val('CW'+angle);
                         });"/>
                    <img src="/static/images/white.png"
                         style="position: absolute; top: 62px; left: 62px; width: 76px; height: 76px;"
                         onclick="$('#$name$rand').val('white')"/>
                </div>''')

        SELECTED = 'checked="checked"'

        if value == 'on':
            onselected = SELECTED
        elif value == 'off':
            offselected = SELECTED
        elif value.startswith('CW') or value == 'white':
            cwselected = SELECTED
            cwhide = 'block'

        return mark_safe(tpl.safe_substitute(name=name, value=value,
                                             rand=random.randint(0, 67234433),
                                             on=_('On'), off=_('Off'), color=_('Color'),
                                             onselected=onselected, offselected=offselected, cwselected=cwselected,
                                             cwhide=cwhide
        ))