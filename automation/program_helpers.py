from django.forms.models import modelformset_factory, ModelForm
from automation.models import Program


def ProgramFormSet(*args, **kwargs):
    program_form_set = modelformset_factory(Program, can_delete=True)
    return program_form_set(*args, **kwargs)


class ProgramForm(ModelForm):
    class Meta:
        model = Program