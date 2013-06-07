from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
import operator
from automation.plugin_mounts import InputBlockFunction, LogicBlockFunction, OutputBlockFunction
from automation.views import InputDeviceStstusChangeView, InputScenarioExecutedView, InputInputExecutedView,\
    InputTimerExecutedView, OutputDeviceStstusChangeView, InputTemperatureChangedView
import desktop.plugin_mounts as desktop_mounts

NAME = ('automation', _('Automation'))

VERSION = (0.1, '0.1')

FEATURES = (
    'desktop.settings.menu',
)


DESKTOP_SETTINGS_MENU = (NAME[0], NAME[1], 'automation_programs'),


class AutomationSettingsItem(desktop_mounts.SettingsMenuItem):
    label = _('Automation')
    setting = 'automation'
    identifier = 'automation_settings_menu_item'
    url = reverse('automation_programs')


class InputDeviceStatusChange(InputBlockFunction):
    label = _('Device Status Change')
    identifier = 'automation_device_status_change'

    settings_view = InputDeviceStstusChangeView


class InputInputExecuted(InputBlockFunction):
    label = _('Input Executed')
    identifier = 'automation_input_executed'

    settings_view = InputInputExecutedView

    def get_label(self, model):
        return _('Input\nExecuted\n%(model)s') % {'model': model.action_object.name}


class InputScenarioExecuted(InputBlockFunction):
    label = _('Scenario Executed')
    identifier = 'automation_scenario_executed'

    settings_view = InputScenarioExecutedView

    def get_label(self, model):
        return _('Scenario\nExecuted\n%(model)s') % {'model': model.action_object.name}


class InputTemperatureChanged(InputBlockFunction):
    label = _('Temperature Changed')
    identifier = 'automation_temperature_changed'

    settings_view = InputTemperatureChangedView

    triggers = {
        0: (_('Any change'), _('changed')),
        1: (_('Temperature over or equal to'), '>='),
        2: (_('Temperature lower or equal to'), '<='),
        3: (_('Temperature between'), '-'),
    }

    def get_label(self, model):
        trigger = model.get_data('trigger', 0)
        if trigger == 0:
            return _('Thermometer\n%(model)s\n%(trigger)s') %\
                {'model': model.action_object.name,
                 'trigger': self.triggers[trigger][1]}
        elif trigger in [1, 2]:
            return _('Thermometer\n%(model)s\nTemp %(trigger)s %(temperature)s') %\
                {'model': model.action_object.name,
                 'trigger': self.triggers[trigger][1],
                 'temperature': model.get_data('temperature', 0)}
        elif trigger == 3:
            return _('Thermometer\n%(model)s\n%(start)s %(trigger)s %(end)s') %\
                {'model': model.action_object.name,
                 'trigger': self.triggers[trigger][1],
                 'start': model.get_data('start', 0),
                 'end': model.get_data('end', 0)}
        else:
            return _('Error')

    def check_status(self, model, temperature):
        trigger = model.get_data('trigger', 0)
        if trigger == 0:
            return True, False
        if trigger == 1:
            set_temp = model.get_data('temperature', 0)
            return (temperature >= set_temp), True
        if trigger == 2:
            set_temp = model.get_data('temperature', 0)
            return (temperature <= set_temp), True
        if trigger == 3:
            start = model.get_data('start', 0)
            end = model.get_data('end', 0)
            return (start <= temperature <= end), True


class InputTimertExecuted(InputBlockFunction):
    label = _('Timer Executed')
    identifier = 'automation_timer_executed'

    settings_view = InputTimerExecutedView

    def get_label(self, model):
        return _('Timer\nExecuted\n%(model)s') % {'model': model.action_object.name}


class LogicAnd(LogicBlockFunction):
    label = _('AND')
    identifier = 'automation_and'

    def get_label(self, model):
        return _('AND')

    def check_logic(self, inputs):
        return reduce(operator.and_, inputs)


class LogicOr(LogicBlockFunction):
    label = _('OR')
    identifier = 'automation_or'

    def get_label(self, model):
        return _('OR')

    def check_logic(self, inputs):
        return reduce(operator.or_, inputs)


class LogicNand(LogicBlockFunction):
    label = _('NAND')
    identifier = 'automation_nand'

    def get_label(self, model):
        return _('NAND')

    def check_logic(self, inputs):
        return not reduce(operator.and_, inputs)


class LogicNor(LogicBlockFunction):
    label = _('NOR')
    identifier = 'automation_nor'

    def get_label(self, model):
        return _('NOR')

    def check_logic(self, inputs):
        return not reduce(operator.or_, inputs)


class OutputExecuteDevice(OutputBlockFunction):
    label = _('Execute Device')
    identifier = 'automation_execute_device'

    settings_view = OutputDeviceStstusChangeView

    def get_label(self, model):
        return _('Turn Device\n%(model)s\n%(action)s') % {'model': model.action_object.name,
                                                          'action': model.get_data('action', '')}

    def do_action(self, model):
        device = model.action_object
        action = model.get_data('action', '')
        device.object.action(action=action)


class OutputSetDeviceStatus(OutputBlockFunction):
    label = _('Set Device Status')
    identifier = 'automation_set_device_status'

    settings_view = OutputDeviceStstusChangeView

    def get_label(self, model):
        return _('Set Device\n%(model)s\n%(action)s') % {'model': model.action_object.name,
                                                         'action': model.get_data('action', '')}

    def do_action(self, model):
        device = model.action_object
        action = model.get_data('action', '')
        device.set_status(action)


class OutputExecuteScenario(OutputBlockFunction):
    label = _('Execute Scenario')
    identifier = 'automation_execute_scenario'

    settings_view = InputScenarioExecutedView

    def get_label(self, model):
        return _('Execute\nScenario\n%(model)s') % {'model': model.action_object.name}

    def do_action(self, model):
        scenario = model.action_object
        scenario.execute()