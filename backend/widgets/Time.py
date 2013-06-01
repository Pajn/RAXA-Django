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
from django.forms import widgets
from RAXA.settings import TIMER_MINUTES_BETWEEN


class Time(widgets.MultiWidget):
    def generate_hours(self):
        self.hours = []
        for i in range(0, 24):
            self.hours.append((str(i), str(i).zfill(2)))

    def generate_minutes(self):
        self.minutes = []
        for i in range(0, 60, TIMER_MINUTES_BETWEEN):
            self.minutes.append((str(i), str(i).zfill(2)))

    def __init__(self, attrs=None, mode=0):
        self.generate_hours()
        self.generate_minutes()

        _widgets = (
            widgets.Select(attrs=attrs, choices=self.hours),
            widgets.Select(attrs=attrs, choices=self.minutes),
        )
        super(Time, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.hour, value.minute]
        return [None, None]

    def format_output(self, rendered_widgets):
        prefix = '<table style="display:inline-table; margin: 0; padding: 0; border 0; border-spacing: 0;"><tr>'
        sufix = '</tr></table>'
        join = ''
        for widget in rendered_widgets:
            join = join + '<td>' + widget + '</td>'

        return prefix + join + sufix

    def value_from_datadict(self, data, files, name):
        line_list = [widget.value_from_datadict(data, files, name + '_%s' % i) for i, widget in enumerate(self.widgets)]
        return line_list[0] + ':' + line_list[1]