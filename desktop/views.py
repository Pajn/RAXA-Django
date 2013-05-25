from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext as _
from backend.models import ConnectorFormSet, InputForm, ThermometerFormSet, RoomFormSet, FloorFormSet
from backend.models.Connector import Connector
from backend.models.Device import Device, DeviceForm, DeviceFormNew
from backend.models.Input import Input
from backend.models.Room import Room, Floor
from backend.models.Scenario import Scenario, ScenarioFormSet, ScenarioDevice, ScenarioDeviceFormNew,\
    ScenarioDeviceFormAction
from backend.models.Timer import Timer, TimerForm
from backend.io.connector import scan_connectors
from backend.models.User import SecurityForm, ThemeForm
from backend.system.network import NetworkForm
from backend.widgets import OnOff, OnOffDimLevel
from backend.widgets.OnOffColorWheel import OnOffColorWheel
from common.models.Theme import ThemeFormSet
from common.models import Temp
from common.models.Furniture import Furniture, FurnitureForm
from common.models.Plan import PlanForm, Plan
from common.models.Temp import TempForm
from desktop.model_helpers.floors import floor_select


class DesktopView(TemplateView):
    template_name = 'desktop/index.html'
    template_args = {}

    floors = Floor.objects.all()
    scenarios = Scenario.objects.all()
    percent = (98 - scenarios.__len__()) / (scenarios.__len__() + 1)

    def on_request(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):
        self.on_request(request, *args, **kwargs)
        return super(DesktopView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.on_request(request, *args, **kwargs)
        return super(DesktopView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DesktopView, self).get_context_data(**kwargs)

        context.update(self.template_args)

        context['scenarios'] = self.scenarios
        context['floors'] = self.floors
        context['percent'] = self.percent
        context['theme'] = self.request.session['theme']

        return context


class DevicesView(TemplateView):
    template_name = 'desktop/devices.html'
    room = None

    def get_context_data(self, **kwargs):
        context = super(DevicesView, self).get_context_data(**kwargs)

        try:
            context['room'] = get_object_or_404(Room, id=kwargs['room'])
            context['devices'] = Device.objects.filter(room=kwargs['room'])
        except KeyError:
            context['room'] = None
            context['devices'] = Device.objects.all()

        return context


class SettingsView(DesktopView):
    setting = None
    template_finder = 'desktop/settings/%(setting)s.html'

    def on_get(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):
        self.template_name = 'desktop/settings.html'
        self.on_get(request, *args, **kwargs)
        return super(SettingsView, self).get(request, *args, **kwargs)

    def on_post(self, request, *args, **kwargs):
        return False

    def post(self, request, *args, **kwargs):
        full = self.on_post(request, *args, **kwargs)
        if self.setting is None or full:
            self.template_name = 'desktop/settings.html'
        else:
            self.template_name = self.template_finder % {'setting': self.setting}
        return super(SettingsView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SettingsView, self).get_context_data(**kwargs)
        context['setting'] = self.setting
        return context


class SubSettingsView(SettingsView):
    setting = None
    subsetting = None
    default = 'settings'

    def __init__(self, **kwargs):
        super(SubSettingsView, self).__init__(**kwargs)
        # Swap setting and subsetting so subclasses stays compatible with subclasses of SettingsView
        self.setting, self.subsetting = self.subsetting, self.setting

    def get_context_data(self, **kwargs):
        context = super(SubSettingsView, self).get_context_data(**kwargs)
        context['subsetting'] = self.subsetting
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.subsetting is None:
            return redirect(reverse(self.default))

        return super(SubSettingsView, self).dispatch(request, *args, **kwargs)


class SystemSettingsView(SubSettingsView):
    subsetting = 'system'
    default = 'system_connectors'


class RoomSettingsView(SubSettingsView):
    subsetting = 'room'
    default = 'room_rooms'


class DevicesSettingsView(SettingsView):
    setting = 'devices'

    template_args = {
        'devices': Device.objects.all().select_related('room__floor'),
        'form': DeviceFormNew()
    }


class DeviceSettingsView(SettingsView):
    setting = 'device'

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('settings_devices'))

    def post(self, request, *args, **kwargs):
        if 'id' in request.POST and request.POST['id'] != 'None':
            device = get_object_or_404(Device, pk=request.POST['id'])
            if 'delete' in request.POST:
                device.delete()
                return HttpResponseRedirect(reverse('settings_devices'))
            elif 'save' in request.POST:
                form = DeviceForm(request.POST, instance=device)
                form.fields['code'].widget = device.object.CODE_WIDGET()
                form.fields['action'].widget = device.object.ACTION_WIDGET()

                if form.is_valid():
                    form.save()
                return HttpResponseRedirect(reverse('settings_devices'))
            elif 'sync' in request.POST:
                device.object.action(action='sync')

            form = DeviceForm(instance=device)
            form.fields['code'].widget = device.object.CODE_WIDGET()
            form.fields['action'].widget = device.object.ACTION_WIDGET()
            self.template_args['device'] = device
            self.template_args['form'] = form
        else:
            device = Device(type=request.POST['type'])
            device.object.new()

            if 'add' in request.POST:
                form = DeviceForm(request.POST, instance=device)
            else:
                form = DeviceForm(instance=device)

            form.fields['code'].widget = device.object.CODE_WIDGET()
            form.fields['action'].widget = device.object.ACTION_WIDGET()

            if 'add' in request.POST:
                if form.is_valid():
                    form.save()
                return HttpResponseRedirect(reverse('settings_devices'))
            else:
                self.template_args['device'] = device
                self.template_args['form'] = form
                self.template_args['add'] = True
        return super(DeviceSettingsView, self).post(request, *args, **kwargs)


class ScenariosSettingsView(SubSettingsView):
    subsetting = 'scenarios'
    default = 'settings_scenarios'


class EditScenariosSettingsView(ScenariosSettingsView):
    setting = 'scenarios_edit'

    template_args = {
        'formset': ScenarioFormSet()
    }

    def on_post(self, request, *args, **kwargs):
        if 'save' in request.POST:
            formset = ScenarioFormSet(request.POST)
            if formset.is_valid():
                formset.save()

            self.template_args['formset'] = formset
            return True


class ScenarioSettingsView(ScenariosSettingsView):
    setting = 'scenario'

    def on_request(self, request, *args, **kwargs):
        self.template_args['scenario'] = get_object_or_404(Scenario, id=kwargs['id'])
        self.template_args['scenariodevices'] = ScenarioDevice.objects.select_related().filter(scenario=kwargs['id'])
        self.template_args['form'] = ScenarioDeviceFormNew()

    def post(self, request, *args, **kwargs):
        if 'add' in request.POST:
            form = ScenarioDeviceFormNew(request.POST)
            if form.is_valid():
                device = form.cleaned_data['device']
                if 'action' in request.POST:
                    action = request.POST['action']
                else:
                    action = 'off'
                newinstance = ScenarioDevice(device=device, scenario=self.template_args['scenario'], action=action)
                newinstance.save()
                return HttpResponseRedirect(reverse('settings_scenario', kwargs={'id': kwargs['id']}))
        return super(ScenarioSettingsView, self).post(request, *args, **kwargs)


class ScenarioDeviceSettingsView(SettingsView):
    setting = 'scenariodevice'

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('settings_scenarios'))

    def post(self, request, *args, **kwargs):
        if 'id' in request.POST:
            scenario_device = get_object_or_404(ScenarioDevice, pk=request.POST['id'])
            form = ScenarioDeviceFormAction(instance=scenario_device)
            if 'delete' in request.POST:
                scenario_device.delete()
                return HttpResponseRedirect(reverse('settings_scenario', kwargs={'id': scenario_device.scenario.id}))
            elif 'save' in request.POST:
                form = ScenarioDeviceFormAction(request.POST, instance=scenario_device)
                if form.is_valid():
                    form.save()
                return HttpResponseRedirect(reverse('settings_scenario', kwargs={'id': scenario_device.scenario.id}))
            self.template_args['form'] = form
            self.template_args['scenario_device'] = scenario_device
        return super(ScenarioDeviceSettingsView, self).post(request, *args, **kwargs)


class InputsSettingsView(SettingsView):
    setting = 'inputs'

    template_args = {
        'inputs': Input.objects.exclude(pk=1)
    }


class InputSettingsView(SettingsView):
    setting = 'input'

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('settings_inputs'))

    def post(self, request, *args, **kwargs):
        if 'id' in request.POST:
            input = get_object_or_404(Input, id=request.POST['id'])
            if 'delete' in request.POST:
                input.delete()
                return HttpResponseRedirect(reverse('settings_inputs'))
            elif 'save' in request.POST:
                postdata = request.POST.copy()
                postdata['action_object'] = postdata['device_scenario']

                form = InputForm(postdata, instance=input)

                if form.is_valid():
                    form.save()
                return HttpResponseRedirect(reverse('settings_inputs'))

            form = InputForm(instance=input)
            self.template_args['input'] = input
            self.template_args['form'] = form
        else:
            if 'scan' in request.POST:
                scan = Input.scan()
                if scan is None:
                    return HttpResponse('<input type="button" value="%s" onclick="scan()"/>' % _('Scan'))
                else:
                    input = Input()
                    input.protocol = scan.protocol
                    input.data = scan.data
                    form = InputForm(instance=input)
                    self.template_args['add'] = True
            elif 'add' in request.POST:
                postdata = request.POST.copy()
                postdata['device_scenario'] = postdata['action_object']

                input = Input()
                form = InputForm(postdata, instance=input)

                if form.is_valid():
                    form.save()
                return HttpResponseRedirect(reverse('settings_inputs'))
            else:
                return HttpResponseRedirect(reverse('settings_inputs'))
            self.template_args['input'] = input
            self.template_args['form'] = form
        return super(InputSettingsView, self).post(request, *args, **kwargs)


class TimersSettingsView(SettingsView):
    setting = 'timers'

    template_args = {
        'timers': Timer.objects.all(),
        'form': TimerForm()
    }


class TimerSettingsView(SettingsView):
    setting = 'timer'

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('settings_timers'))

    def post(self, request, *args, **kwargs):
        if 'id' in request.POST:
            timer = get_object_or_404(Timer, id=request.POST['id'])
            if 'delete' in request.POST:
                timer.delete()
                return HttpResponseRedirect(reverse('settings_timers'))
            elif 'save' in request.POST:
                postdata = request.POST.copy()
                postdata['action_object'] = postdata['device_scenario']

                form = TimerForm(postdata, instance=timer)

                if form.is_valid():
                    form.save()
                return HttpResponseRedirect(reverse('settings_timers'))

            form = TimerForm(instance=timer)
            self.template_args['timer'] = timer
            self.template_args['form'] = form
        else:
            postdata = request.POST.copy()
            postdata['device_scenario'] = postdata['action_object']

            timer = Timer()
            form = TimerForm(postdata, instance=timer)

            if form.is_valid():
                form.save()
            return HttpResponseRedirect(reverse('settings_timers'))
        return super(TimerSettingsView, self).post(request, *args, **kwargs)


class ThermometersSettingsView(SettingsView):
    setting = 'thermometers'

    template_args = {
        'formset': ThermometerFormSet(),
    }

    def on_post(self, request, *args, **kwargs):
        if 'save' in request.POST:
            formset = ThermometerFormSet(request.POST)
            if formset.is_valid():
                formset.save()
                self.template_args['formset'] = ThermometerFormSet()
            else:
                self.template_args['formset'] = formset
            return True


class FurnitureSettingsView(SettingsView):
    setting = 'furniture'

    floor = None

    template_args = {
        'dot_form': FurnitureForm(),
        'temp_form': TempForm()
    }

    def on_post(self, request, *args, **kwargs):
        if 'floor' in request.POST:
            self.floor = request.POST['floor']
        if 'id' in request.POST:
            id = request.POST['id']
            if request.POST['furniture_type'] == 'dot':
                object = get_object_or_404(Furniture, pk=id)
                object.delete()
            elif request.POST['furniture_type'] == 'temp':
                object = get_object_or_404(Temp, pk=id)
                object.delete()
        if 'save' in request.POST:
            if request.POST['furniture_type'] == 'dot':
                form = FurnitureForm(request.POST)
            elif request.POST['furniture_type'] == 'temp':
                form = TempForm(request.POST)
            else:
                return

            if form.is_valid():
                form.save()
            return True

    def get_context_data(self, **kwargs):
        context = super(FurnitureSettingsView, self).get_context_data(**kwargs)
        try:
            floor = kwargs['floor']
        except KeyError:
            floor = self.floor
        context['selectfloor'] = floor_select(floor)

        return context


class ConnectorsSettingsView(SystemSettingsView):
    setting = 'connectors'

    template_args = {
        'formset': ConnectorFormSet()
    }

    def on_post(self, request, *args, **kwargs):
        if 'save' in request.POST:
            formset = ThermometerFormSet(request.POST)
            if formset.is_valid():
                formset.save()
            self.template_args['formset'] = formset
            return True
        elif 'search' in request.POST:
            scan_connectors()
            self.template_args['formset'] = ConnectorFormSet()
        elif 'update' in request.POST:
            connector = get_object_or_404(Connector, id=request.POST['update'])
            connector.object.update()


class NetworkSettingsView(SystemSettingsView):
    setting = 'network'

    template_args = {
        'form': NetworkForm()
    }

    def on_post(self, request, *args, **kwargs):
        if 'save' in request.POST:
            form = NetworkForm(request.POST)
            if form.is_valid():
                form.save()
            self.template_args['form'] = form
            return True


class SecuritySettingsView(SystemSettingsView):
    setting = 'security'

    template_args = {
        'form': SecurityForm()
    }

    def on_post(self, request, *args, **kwargs):
        if 'save' in request.POST:
            form = SecurityForm(request.POST, instance=request.session['user'])
            if form.is_valid():
                form.save()
            self.template_args['form'] = form
            return True
        elif 'logout' in request.POST:
            request.session['auth'] = 0
            return True


class ThemesSettingsView(SystemSettingsView):
    setting = 'themes'

    template_args = {
        'reload': False
    }

    def on_request(self, request, *args, **kwargs):
        self.template_args['formset'] = ThemeFormSet(request.session['theme'].id)

    def on_post(self, request, *args, **kwargs):
        if 'save' in request.POST:
            formset = ThemeFormSet(request.session['user'].theme.id, request.POST, request.FILES)
            if formset.is_valid():
                formset.save()
                self.template_args['reload'] = True

            form = ThemeForm(request.POST, instance=request.session['user'])
            if form.is_valid():
                form.save()
                self.template_args['reload'] = True
            self.template_args['formset'] = formset
            return True


class RoomsSettingsView(RoomSettingsView):
    setting = 'rooms'

    template_args = {
        'formset': RoomFormSet()
    }

    def on_post(self, request, *args, **kwargs):
        if 'save' in request.POST:
            formset = RoomFormSet(request.POST)
            if formset.is_valid():
                formset.save()
            self.template_args['formset'] = formset
            return True


class FloorsSettingsView(RoomSettingsView):
    setting = 'floors'

    template_args = {
        'formset': FloorFormSet()
    }

    def on_post(self, request, *args, **kwargs):
        if 'save' in request.POST:
            formset = FloorFormSet(request.POST, request.FILES)
            if formset.is_valid():
                formset.save()
            self.template_args['formset'] = formset
            return True


class PlanSettingsView(RoomSettingsView):
    setting = 'plan'

    floor = None

    template_args = {
        'form': PlanForm()
    }

    def on_post(self, request, *args, **kwargs):
        if 'floor' in request.POST:
            self.floor = request.POST['floor']
        if 'id' in request.POST:
            plan = get_object_or_404(Plan, id=request.POST['id'])
            plan.delete()
        if 'save' in request.POST:
            form = PlanForm(request.POST)

            if form.is_valid():
                form.save()
            else:
                self.template_args['form'] = form
            return True

    def get_context_data(self, **kwargs):
        context = super(PlanSettingsView, self).get_context_data(**kwargs)
        try:
            floor = kwargs['floor']
        except KeyError:
            floor = self.floor
        context['selectfloor'] = floor_select(floor)

        return context


def widget_action(request):
    if request.method == 'POST' and 'device' in request.POST:
        device = get_object_or_404(Device, id=request.POST['device'])

        if 'color_wheel' in device.object.SUPPORTED_ACTIONS:
            widget = OnOffColorWheel(device=device)
        elif 'dim_level' in device.object.SUPPORTED_ACTIONS:
            widget = OnOffDimLevel(device=device)
        else:
            widget = OnOff()
    else:
        raise Http404('No device specified')

    return HttpResponse(widget.render('action', 'off'))