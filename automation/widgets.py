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
from django.core.urlresolvers import reverse
from string import Template
from django.forms import Widget
from django.utils.safestring import mark_safe


class DeviceActionWidget(Widget):
    def __init__(self, value=None, *args, **kwargs):
        super(DeviceActionWidget, self).__init__(*args, **kwargs)

        self.value = value

    def render(self, name, value, attrs=None):

        tpl = Template('''
            <input type="hidden" id="id_$name" name="$name" value="$value" />
            <div id="id_div_$name"></div>
            <script>
                $('#id_action_object').on('change', function() {
                    get_action_widget();
                });
                function get_action_widget() {
                    var id = $('#id_action_object').val();
                    var value = $('#id_$name').val();
                    if (id == '') {
                        $('#id_div_$name').html('');
                        return false;
                    }
                    $('#id_div_$name').load('$url', {'device': id, 'value': value}, function () {
                        fix_sliders();
                    });
                }
                get_action_widget();
                function fix_sliders() {
                    $('input[type="range"]').each(function (index, input) {
                        var $input, $label, $slider, $container;

                        $input = $(input);

                        $container = $('<div class="slider" style="width: 195px"/>');
                        $label = $('<span class="label ui-widget-content ui-corner-all">' + parseInt($input.attr('value'), 10) + '</span>');

                        //Create a new div, turn it into a slider, and set its attributes based on
                        //the attributes of the input.
                        $slider = $('<div style="float: right;width: 150px"/>').slider({
                            min: parseInt($input.attr('min'), 10),
                            max: parseInt($input.attr('max'), 10),
                            value: parseInt($input.attr('value'), 10),
                            step: parseInt($input.attr('step'), 10),
                            slide: function (event, ui) {
                                //Keep the value of the input[type=range] in sync with the slider.
                                //$(this).prev('input').val(ui.value);
                                $input.val(ui.value);
                                $input.change();
                                $label.text(ui.value);
                            }
                        });

                        //Append the slider after the input and hide the input.  The user will only
                        //interact with the slider.
                        $input.hide();
                        $input.after($container);
                        $container.append($label);
                        $label.after($slider);
                    });
                }
            </script>''')

        return mark_safe(tpl.safe_substitute(name=name, value=value, url=reverse('desktop.views.widget_action')))


class ThermometerHelperWidget(Widget):
    is_hidden = True

    def render(self, name, value, attrs=None):

        return mark_safe('''
            <script>
                $('input[name=trigger]').on('change', function() {
                    show_hide_fields();
                });
                function show_hide_fields() {
                    var val = parseInt($('input[name=trigger]:checked').val());
                    switch(val) {
                        case 0:
                            $('#id_temperature').parent().hide();
                            $('#id_start').parent().hide();
                            $('#id_end').parent().hide();
                            break;
                        case 1:
                        case 2:
                            $('#id_temperature').parent().show();
                            $('#id_start').parent().hide();
                            $('#id_end').parent().hide();
                            break;
                        case 3:
                            $('#id_temperature').parent().hide();
                            $('#id_start').parent().show();
                            $('#id_end').parent().show();
                            break;
                    }
                }
                show_hide_fields();
            </script>''')


class CounterHelperWidget(Widget):
    is_hidden = True

    def render(self, name, value, attrs=None):

        return mark_safe('''
            <script>
                $('input[name=trigger]').on('change', function() {
                    show_hide_fields();
                });
                function show_hide_fields() {
                    var val = parseInt($('input[name=trigger]:checked').val());
                    switch(val) {
                        case 0:
                        case 1:
                        case 2:
                            $('#id_value').parent().show();
                            $('#id_start').parent().hide();
                            $('#id_end').parent().hide();
                            break;
                        case 3:
                            $('#id_value').parent().hide();
                            $('#id_start').parent().show();
                            $('#id_end').parent().show();
                            break;
                        case 4:
                        case 5:
                        case 6:
                            $('#id_value').parent().hide();
                            $('#id_start').parent().hide();
                            $('#id_end').parent().hide();
                            break;
                    }
                }
                show_hide_fields();
            </script>''')