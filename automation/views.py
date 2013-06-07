from django.utils.encoding import force_unicode
import json
from django.template.loader import render_to_string
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, View
from automation import models, logic_helpers
from automation.forms import InputDeviceStstusChangeForm, NoSettingsForm, InputScenarioExecutedForm,\
    InputInputExecutedForm, InputTimerExecutedForm, OutputDeviceStstusChangeForm, InputTemperatureChangedForm
from automation.models import LogicBlock, Link
from automation.plugin_mounts import InputBlockFunction, LogicBlockFunction, OutputBlockFunction
from automation.program_helpers import ProgramFormSet
from desktop.views import SubSettingsView


class Automation(SubSettingsView):
    subsetting = 'automation'
    default = 'automation_programs'
    template_finder = 'automation/settings/{0}.html'
    app = 'automation'

    def get_context_data(self, **kwargs):
        context = super(Automation, self).get_context_data(**kwargs)
        context['programs'] = models.Program.objects.all()
        return context


class Programs(Automation):
    setting = 'programs'

    def __init__(self, **kwargs):
        super(Programs, self).__init__(**kwargs)
        self.template_args['formset'] = ProgramFormSet()

    def on_post(self, request, *args, **kwargs):
        if 'save' in request.POST:
            formset = ProgramFormSet(request.POST)
            if formset.is_valid():
                formset.save()
                self.template_args['formset'] = ProgramFormSet()
            else:
                self.template_args['formset'] = formset
            return True


class Program(Automation):
    setting = 'program'

    template_args = {
        'logic_helpers': logic_helpers,
    }

    def on_request(self, request, *args, **kwargs):
        self.template_args['program'] = get_object_or_404(models.Program, id=kwargs['id'])


class Drawingboard(TemplateView):
    template_name = 'automation/drawingboard.svg'

    def get_context_data(self, **kwargs):
        context = super(Drawingboard, self).get_context_data(**kwargs)
        context['blocks'] = LogicBlock.objects.filter(program=kwargs['id'])
        context['block_types'] = logic_helpers.LogicBlockTypes
        return context


class LogicBlockDelete(View):
    def post(self, request, *args, **kwargs):
        block = get_object_or_404(LogicBlock, id=request.POST['id'])
        block.delete()
        return HttpResponse(json.dumps({'saved': True}), mimetype="application/json")


class LogicLink(View):
    def post(self, request, *args, **kwargs):
        link = Link()
        link.start = get_object_or_404(LogicBlock, id=request.POST['start'])
        link.end = get_object_or_404(LogicBlock, id=request.POST['end'])
        link.save()
        return HttpResponse(json.dumps({'saved': True, 'id': link.id}), mimetype="application/json")


class FunctionSettings(TemplateView):
    request = None

    def dispatch(self, request, *args, **kwargs):
        type = self.request.REQUEST['type']
        function = self.request.REQUEST['function']

        if type == str(logic_helpers.LogicBlockTypes.input):
            plugin = InputBlockFunction.get_plugin(function)
        elif type == str(logic_helpers.LogicBlockTypes.gate):
            plugin = LogicBlockFunction.get_plugin(function)
        elif type == str(logic_helpers.LogicBlockTypes.output):
            plugin = OutputBlockFunction.get_plugin(function)
        else:
            raise Http404()

        view = getattr(plugin, 'settings_view', NoSettings)
        return view.as_view()(request, plugin=plugin, *args, **kwargs)


class NoSettings(TemplateView):
    template_name = 'automation/settings_form.html'
    form = NoSettingsForm
    context = None

    def post(self, request, *args, **kwargs):
        response = {'saved': False}

        form = self.form(data=request.POST, plugin=self.kwargs['plugin'])
        if form.is_valid():
            form.save()
            response['saved'] = True
            response['id'] = form.instance.id
            response['label'] = force_unicode(self.kwargs['plugin'].get_label(form.instance)).split('\n')
        self.context = {'form': form}

        context = self.get_context_data(**kwargs)
        response['html'] = render_to_string(self.template_name, context)
        return HttpResponse(json.dumps(response), mimetype="application/json")

    def get_context_data(self, **kwargs):
        context = super(NoSettings, self).get_context_data(**kwargs)
        if self.context is None:
            context['form'] = self.form(plugin=self.kwargs['plugin'])
        else:
            context.update(self.context)
        return context


class InputDeviceStstusChangeView(NoSettings):
    form = InputDeviceStstusChangeForm


class InputInputExecutedView(NoSettings):
    form = InputInputExecutedForm


class InputScenarioExecutedView(NoSettings):
    form = InputScenarioExecutedForm


class InputTemperatureChangedView(NoSettings):
    form = InputTemperatureChangedForm


class InputTimerExecutedView(NoSettings):
    form = InputTimerExecutedForm


class OutputDeviceStstusChangeView(NoSettings):
    form = OutputDeviceStstusChangeForm