import threading
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from automation.logic_helpers import LogicBlockTypes
from automation.models import LogicBlock, Link
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
        affected_blocks = LogicBlock.objects.filter(type=LogicBlockTypes.input,
                                                    function=self.function,
                                                    object_id=self.action_object.id,
                                                    content_type=ContentType.objects.get_for_model(self.action_object)
                                                    ).values_list('id', flat=True)

        if affected_blocks.__len__() < 1:
            return

        # Prefetch all blocks and keep only a single instance for every block
        all_blocks = {}
        links = Link.objects.all().select_related('start', 'end')
        for link in links:
            if not link.start.id in all_blocks:
                all_blocks[link.start.id] = link.start
                all_blocks[link.start.id].input_list = []
                all_blocks[link.start.id].output_list = []
            if not link.end.id in all_blocks:
                all_blocks[link.end.id] = link.end
                all_blocks[link.end.id].input_list = []
                all_blocks[link.end.id].output_list = []
            all_blocks[link.start.id].output_list.append(link.end)
            all_blocks[link.end.id].input_list.append(link.start)

        self.affected_blocks = []

        for block in affected_blocks:
            self.affected_blocks.append(all_blocks[block])

        self.set_status()
        self.run_program()

    def set_status(self):
        for block in self.affected_blocks:
            block.active = True

    def run_program(self):
        for block in self.affected_blocks:
            program_thread = RunProgram(block)
            program_thread.start()


class CheckDeviceStatusBlock(PulseBlock):
    def __init__(self, action_object, status):
        super(CheckDeviceStatusBlock, self).__init__('automation_device_status_change', action_object)
        self.status = status

    def set_status(self):
        transaction.enter_transaction_management()
        transaction.managed(True)

        for block in self.affected_blocks:
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

        for block in self.affected_blocks:
            block.active, save = block.plugin.check_status(block, self.temperature)
            if save:
                block.save()

        transaction.commit()

        transaction.leave_transaction_management()


class CheckMemoryStatusBlock(PulseBlock):
    def __init__(self, action_object, status):
        super(CheckMemoryStatusBlock, self).__init__('automation_input_rs_memory', action_object)
        self.status = status

    def set_status(self):
        transaction.enter_transaction_management()
        transaction.managed(True)

        for block in self.affected_blocks:
            block.active, save = block.plugin.check_status(block, self.status)
            if save:
                block.save()

        transaction.commit()

        transaction.leave_transaction_management()


class CheckCounterStatusBlock(PulseBlock):
    def __init__(self, action_object, value, change):
        super(CheckCounterStatusBlock, self).__init__('automation_input_counter', action_object)
        self.value = value
        self.change = change

    def set_status(self):
        transaction.enter_transaction_management()
        transaction.managed(True)

        for block in self.affected_blocks:
            block.active, save = block.plugin.check_status(block, self.value, self.change)
            if save:
                block.save()

        transaction.commit()

        transaction.leave_transaction_management()