from django.db import connection
from automation.logic_helpers import LogicBlockTypes


def check_down(block):
    print connection.queries
    for output in block.output_list:
        if output.type == LogicBlockTypes.output:
            if block.active:
                output.plugin.do_action(output)
        elif output.type == LogicBlockTypes.gate:
            check_down(check_gate(output))


def check_gate(block):
    inputs = []

    for input in block.input_list:
        if input.type == LogicBlockTypes.input:
            inputs.append(input.active)
        elif input.type == LogicBlockTypes.gate:
            inputs.append(check_gate(input))

    block.active = block.plugin.check_logic(inputs, block)
    return block