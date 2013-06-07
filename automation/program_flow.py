from automation.logic_helpers import LogicBlockTypes
from automation.models import LogicBlock


def check_down(block):
    assert isinstance(block, LogicBlock)
    for link in block.outputs.all():
        end = link.end
        if end.type == LogicBlockTypes.output:
            if link.start.active:
                end.plugin.do_action(end)
        elif end.type == LogicBlockTypes.gate:
            check_gate(end)


def check_gate(block):
    inputs = []

    for input in block.inputs.all():
        start = input.start
        if start.type == LogicBlockTypes.input:
            start.append(start.active)
        elif start.type == LogicBlockTypes.gate:
            start.append(check_gate(start))

    block.active = block.plugin.check_logic(inputs)
    return block.active