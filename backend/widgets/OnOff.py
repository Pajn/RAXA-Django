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