from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
import operator
import time
from functools import reduce
from automation.plugin_mounts import InputBlockFunction, LogicBlockFunction, OutputBlockFunction
from automation.signals import rs_memory_change, counter_change
from automation.views import InputDeviceStstusChangeView, InputScenarioExecutedView, InputInputExecutedView,\
    InputTimerExecutedView, OutputDeviceStstusChangeView, InputTemperatureChangedView, OutputRSMemoryView,\
    InputRSMemoryView, InputCounterView, OutputCounterView, LogicDelayView
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


class InputRSMemory(InputBlockFunction):
    label = _('Memory')
    identifier = 'automation_input_rs_memory'

    settings_view = InputRSMemoryView

    triggers = {
        0: (_('Output active state'), ''),
        1: (_('Pulse on change'), _('changed')),
        2: (_('Pulse on high'), _('set')),
        3: (_('Pulse on low'), _('reset')),
    }

    def get_label(self, model):
        trigger = model.get_data('trigger', 0)
        return _('Memory\n%(memory)s\n%(trigger)s') %\
            {'memory': model.action_object.name,
             'trigger': self.triggers[trigger][1]}

    def check_status(self, model, state):
        trigger = model.get_data('trigger', 0)
        memory = model.action_object

        if trigger == 0:
            return memory.get_data('active', False), True
        if trigger == 1:
            return True, False
        if trigger == 2:
            return state, False
        if trigger == 3:
            return not state, False


class InputCounter(InputBlockFunction):
    label = _('Counter')
    identifier = 'automation_input_counter'

    settings_view = InputCounterView

    triggers = {
        0: (_('Output high at value'), _('==')),
        1: (_('Output high above value'), _('>=')),
        2: (_('Output high below value'), _('<=')),
        3: (_('Output high between'), _('-')),
        4: (_('Pulse on change'), _('changed')),
        5: (_('Pulse on increase'), _('increased')),
        6: (_('Pulse on decrease'), _('decreased')),
    }

    def get_label(self, model):
        trigger = model.get_data('trigger', 0)
        if trigger <= 2:
            value = model.get_data('value', 0)
            return _('Counter\n%(counter)s\n%(trigger)s %(value)i') %\
                {'counter': model.action_object.name,
                 'trigger': self.triggers[trigger][1],
                 'value': value}
        if trigger == 3:
            start = model.get_data('start', 0)
            end = model.get_data('end', 0)
            return _('Counter\n%(counter)s\n%(start)i %(trigger)s %(end)i') %\
                {'counter': model.action_object.name,
                 'trigger': self.triggers[trigger][1],
                 'start': start,
                 'end': end}
        else:
            return _('Counter\n%(counter)s\n%(trigger)s') %\
                {'counter': model.action_object.name,
                 'trigger': self.triggers[trigger][1]}

    def check_status(self, model, value, change):
        trigger = model.get_data('trigger', 0)

        if trigger == 0:
            return model.get_data('value', 0) == value, True
        if trigger == 1:
            return value >= model.get_data('value', 0), True
        if trigger == 2:
            return value <= model.get_data('value', 0), True
        if trigger == 3:
            start = model.get_data('start', 0)
            end = model.get_data('end', 0)
            return (start <= value <= end), True
        if trigger == 4:
            return True, False
        if trigger == 5:
            return change > 0, False
        if trigger == 6:
            return change < 0, False


class LogicAnd(LogicBlockFunction):
    label = _('AND')
    identifier = 'automation_and'

    def get_label(self, model):
        return _('AND')

    def check_logic(self, inputs, model):
        return reduce(operator.and_, inputs)


class LogicOr(LogicBlockFunction):
    label = _('OR')
    identifier = 'automation_or'

    def get_label(self, model):
        return _('OR')

    def check_logic(self, inputs, model):
        return reduce(operator.or_, inputs)


class LogicNand(LogicBlockFunction):
    label = _('NAND')
    identifier = 'automation_nand'

    def get_label(self, model):
        return _('NAND')

    def check_logic(self, inputs, model):
        return not reduce(operator.and_, inputs)


class LogicNor(LogicBlockFunction):
    label = _('NOR')
    identifier = 'automation_nor'

    def get_label(self, model):
        return _('NOR')

    def check_logic(self, inputs, model):
        return not reduce(operator.or_, inputs)


class LogicDelay(LogicBlockFunction):
    label = _('Delay')
    identifier = 'automation_delay'

    settings_view = LogicDelayView

    def get_label(self, model):
        return _('Delay\n%(seconds)is') % {'seconds': model.get_data('seconds', 0)}

    def check_logic(self, inputs, model):
        time.sleep(model.get_data('seconds', 0))
        return reduce(operator.or_, inputs)


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


class OutputRSMemory(OutputBlockFunction):
    label = _('Memory')
    identifier = 'automation_output_rs_memory'

    settings_view = OutputRSMemoryView

    actions = {
        0: _('Set'),
        1: _('Reset'),
        2: _('Toggle'),
    }

    def get_label(self, model):
        return _('%(action)s\nMemory\n%(memory)s') % {'action': self.actions[model.get_data('action', 0)],
                                                      'memory': model.action_object.name}

    def do_action(self, model):
        action = model.get_data('action', 0)
        memory = model.action_object

        if action == 0:
            status = True
        elif action == 1:
            status = False
        elif action == 2:
            status = not memory.get_data('active', False)
        else:
            status = False

        memory.put_data('active', status)

        rs_memory_change.send_robust(sender=self, memory=memory, status=status)


class OutputCounter(OutputBlockFunction):
    label = _('Counter')
    identifier = 'automation_output_counter'

    settings_view = OutputCounterView

    actions = {
        0: (_('Set value')),
        1: (_('Change by')),
    }

    def get_label(self, model):
        action = model.get_data('action', 0)
        value = model.get_data('value', 0)
        if action == 0:
            action = '='
        else:
            if value < 0:
                action = '-'
                value *= -1
            else:
                action = '+'
        return _('Counter\n%(counter)s\n%(action)s %(value)i') % {'action': action,
                                                                  'counter': model.action_object.name,
                                                                  'value': value}

    def do_action(self, model):
        action = model.get_data('action', 0)
        counter = model.action_object

        function_value = model.get_data('value', 0)
        counter_value = counter.get_data('value', 0)

        if action == 0:
            value = function_value
            change = function_value - counter_value
        elif action == 1:
            value = counter_value + function_value
            change = function_value
        else:
            value = False
            change = 0

        counter.put_data('value', value)

        counter_change.send_robust(sender=self, counter=counter, value=value, change=change)