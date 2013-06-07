from django.utils.translation import ugettext_lazy as _
from automation.plugin_mounts import InputBlockFunction, OutputBlockFunction, LogicBlockFunction


class LogicBlockTypes():
    input = 1
    output = 2
    gate = 3

    name = {
        input: _('Input'),
        output: _('Output'),
        gate: _('Logic Gate'),
    }

    @property
    def children(cls):
        return {
            cls.input: InputBlockFunction.get_plugins(),
            cls.output: OutputBlockFunction.get_plugins(),
            cls.gate: LogicBlockFunction.get_plugins(),
        }