import threading
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from automation.logic_helpers import LogicBlockTypes
from automation.models import LogicBlock
from automation.program_flow import check_down


class RunProgram(threading.Thread):
    def __init__(self, block):
        super(RunProgram, self).__init__()
        self.block = block

    def run(self):
        check_down(self.block)


class PulseBlock(threading.Thread):
    def __init__(self, function, action_object):
        super(PulseBlock, self).__init__()
        self.type = type
        self.function = function
        self.action_object = action_object

    def run(self):
        self.blocks = LogicBlock.objects.filter(type=LogicBlockTypes.input,
                                                function=self.function,
                                                object_id=self.action_object.id,
                                                content_type=ContentType.objects.get_for_model(self.action_object))
        if self.blocks.__len__() < 1:
            return

        self.set_status()
        self.run_program()

    def set_status(self):
        for block in self.blocks:
            block.active = True

    def run_program(self):
        for block in self.blocks:
            program_thread = RunProgram(block)
            program_thread.start()


class CheckDeviceStatusBlock(PulseBlock):
    def __init__(self, action_object, status):
        super(CheckDeviceStatusBlock, self).__init__('automation_device_status_change', action_object)
        self.status = status

    def set_status(self):
        transaction.enter_transaction_management()
        transaction.managed(True)

        for block in self.blocks:
            block.active, save = block.plugin.check_status(block, self.status)
            if save:
                block.save()

        transaction.commit()

        transaction.leave_transaction_management()


class CheckThermometerStatusBlock(PulseBlock):
    def __init__(self, action_object, temperature):
        super(CheckThermometerStatusBlock, self).__init__('automation_temperature_changed', action_object)
        self.temperature = temperature

    def set_status(self):
        transaction.enter_transaction_management()
        transaction.managed(True)

        for block in self.blocks:
            block.active, save = block.plugin.check_status(block, self.temperature)
            if save:
                block.save()

        transaction.commit()

        transaction.leave_transaction_management()