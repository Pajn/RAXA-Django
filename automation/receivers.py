from django.dispatch import receiver
from automation.program_threads import PulseBlock, CheckDeviceStatusBlock, CheckThermometerStatusBlock,\
    CheckMemoryStatusBlock, CheckCounterStatusBlock
from automation.signals import rs_memory_change, counter_change
from backend.models import device_status_change, input_executed, scenario_executed, temperature_changed, timer_executed


@receiver(device_status_change)
def device_status_change(sender, **kwargs):
    if False:
        device = kwargs['device']
        status = kwargs['status']

        thread = CheckDeviceStatusBlock(action_object=device,
                                        status=status)
        thread.start()


@receiver(input_executed)
def input_executed(sender, **kwargs):
    input = kwargs['input']

    thread = PulseBlock(function='automation_input_executed',
                        action_object=input)
    thread.start()

@receiver(scenario_executed)
def scenario_executed(sender, **kwargs):
    scenario = kwargs['scenario']

    thread = PulseBlock(function='automation_scenario_executed',
                        action_object=scenario)
    thread.start()

@receiver(temperature_changed)
def temperature_changed(sender, **kwargs):
    thermometer = kwargs['thermometer']
    temperature = kwargs['temperature']

    thread = CheckThermometerStatusBlock(action_object=thermometer,
                                         temperature=temperature)
    thread.start()

@receiver(timer_executed)
def timer_executed(sender, **kwargs):
    timer = kwargs['timer']

    thread = PulseBlock(function='automation_timer_executed',
                        action_object=timer)
    thread.start()

@receiver(rs_memory_change)
def rs_memory_change(sender, **kwargs):
    memory = kwargs['memory']
    status = kwargs['status']

    thread = CheckMemoryStatusBlock(action_object=memory,
                                    status=status)
    thread.start()

@receiver(counter_change)
def counter_change(sender, **kwargs):
    counter = kwargs['counter']
    value = kwargs['value']
    change = kwargs['change']

    thread = CheckCounterStatusBlock(action_object=counter,
                                     value=value,
                                     change=change)
    thread.start()