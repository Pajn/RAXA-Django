from django.core.urlresolvers import reverse
from django.forms import Select
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext as _
from backend.models import ConnectorFormSet, InputForm
from backend.models.Device import Device, DeviceForm, DeviceFormNew
from backend.models.Input import Input
from backend.models.Room import Room, Floor
from backend.models.Scenario import Scenario, ScenarioFormSet, ScenarioDevice, ScenarioDeviceFormNew, ScenarioDeviceFormAction
from backend.models.Timer import Timer, TimerForm
from backend.out.connector import scan_connectors
from backend.system import updates
from backend.system.network import NetworkForm
from backend.widgets import OnOff, OnOffDimLevel
from common.models.Furniture import Furniture, FurnitureForm
from common.models.Plan import PlanForm

def index(request, template='desktop/index.html', **kwargs):
    floors = Floor.objects.all()
    scenarios = Scenario.objects.all()
    percent = (98-scenarios.__len__()) / (scenarios.__len__()+1)
    kwargs['scenarios'] = scenarios
    kwargs['floors'] = floors
    kwargs['percent'] = percent
    return render(request, template, kwargs)

def devices(request):
    if request.REQUEST.has_key('room'):
        room = request.REQUEST['room']
        room = get_object_or_404(Room, pk=room)
        list = Device.objects.filter(room=room.id)
    else:
        raise Http404('No room specified')
    return render(request, 'desktop/devices.html', {'list': list, 'room': room})

def setting(request, settings=None, **kwargs):
    return index(request, template='desktop/settings.html', settings=settings, **kwargs)

def settings_index(request):
    return Settings(request).render()

def settings(request, type=None, **kwargs):
    return Settings(request, type=type, **kwargs).render()

def systemsettings(request, type=None, **kwargs):
    return Settings(request, type='system', subtype=type, **kwargs).render()

class Settings():
    template = ''
    kwargs = {}
    full = True

    def __init__(self, request, type=None, subtype=None, **kwargs):
        self.request = request

        if type is None and request.method == 'POST' and 'type' in request.POST:
            self.full = False
            type = request.POST['type']

        if subtype is None and request.method == 'POST' and 'subtype' in request.POST:
            self.full = False
            subtype = request.POST['subtype']

        if type is not None:
            if type == 'devices':
                self.devices()
            elif type == 'scenarios':
                self.scenarios()
            elif type == 'inputs':
                self.inputs()
            elif type == 'timers':
                self.timers()
            elif type == 'system':
                if subtype == 'connectors':
                    self.connectors()
                elif subtype == 'network':
                    self.network()
                elif subtype == 'updates':
                    self.updates()
                else:
                    self.system()
            elif type == 'rooms':
                self.rooms()
            elif type == 'plan' or type == 'furniture':
                self.furniture()

    def render(self):
        if self.full:
            if self.template.startswith('system/'):
                self.template = self.template.split('/')[1]
                return index(self.request, template='desktop/settings.html', settings='system', subsettings=self.template, **self.kwargs)
            else:
                return index(self.request, template='desktop/settings.html', settings=self.template, **self.kwargs)
        else:
            if self.template is None:
                return render(self.request, 'desktop/settings.html')
            elif self.template.startswith('system/'):
                self.template = self.template.split('/')[1]
                print self.template
                return render(self.request, 'desktop/settings/system/%s/%s.html' % (self.template, self.template), self.kwargs)
            else:
                return render(self.request, 'desktop/settings/%s/%s.html' % (self.template, self.template), self.kwargs)

    def devices(self):
        list = Device.objects.select_related().all()
        form = DeviceFormNew()

        self.template = 'devices'
        self.kwargs = {'devices': list, 'form': form}

    def scenarios(self):
        scenarios = Scenario.objects.all()
        formset = ScenarioFormSet()

        self.template = 'scenarios'
        self.kwargs = {'scenarios': scenarios, 'formset': formset}

    def inputs(self):
        list = Input.objects.exclude(pk=0)

        self.template = 'inputs'
        self.kwargs = {'inputs': list}

    def timers(self):
        list = Timer.objects.all()
        form = TimerForm()

        self.template = 'timers'
        self.kwargs = {'timers': list, 'form': form}

    def system(self):
        self.template = 'system'

    def connectors(self):
        if self.request.method == 'POST':
            if 'save' in self.request.POST:
                formset = ConnectorFormSet(self.request.POST)
                if formset.is_valid():
                    formset.save()
            elif 'search' in self.request.POST:
                scan_connectors()

        formset = ConnectorFormSet()

        self.template = 'system/connectors'
        self.kwargs = {'formset': formset}

    def network(self):
        form = NetworkForm()

        if self.request.method == 'POST':
            if 'save' in self.request.POST:
                form = NetworkForm(self.request.POST)
                if form.is_valid():
                    form.save()

        self.template = 'system/network'
        self.kwargs = {'form': form}

    def updates(self):
        if self.request.method == 'POST' and 'update' in self.request.POST:
            update = updates.Update(self.request.POST['version'],self.request.POST['patch'])
            update.apply()

            return HttpResponseRedirect(reverse('desktop.views.index'))

        else:
            current_v = updates.write_version(updates.version())
            checked, update = updates.check()
            if checked:
                head_v = updates.write_version(update.version)
            else:
                head_v = _("Couldn't check")

            self.template = 'system/updates'
            self.kwargs = {'current_v':current_v, 'head_v':head_v, 'update':update}

    def rooms(self):
        floor = None
        form = PlanForm()
        floors = []
        for floor in Floor.objects.all():
            floors.append((floor.id, floor.name))

        if self.request.method == 'POST':
            if 'floor' in self.request.POST:
                floor = self.request.POST['floor']
                print floor
            if 'id' in self.request.POST:
                id = self.request.POST['id']
                object = get_object_or_404(Furniture, pk=id)
                object.delete()
            if 'save' in self.request.POST:
                form = PlanForm(self.request.POST)

                if form.is_valid(): # All validation rules pass
                    form.save()
                    form = PlanForm()

        selectfloor = Select(choices=floors).render('selectfloor', floor, attrs={'id':'selectfloor'})

        self.template = 'rooms'
        self.kwargs = {'selectfloor': selectfloor, 'form':form}

    def furniture(self):
        floor = None
        form = FurnitureForm()
        floors = []
        for floor in Floor.objects.all():
            floors.append((floor.id, floor.name))

        if self.request.method == 'POST':
            if 'floor' in self.request.POST:
                floor = self.request.POST['floor']
                print floor
            if 'id' in self.request.POST:
                id = self.request.POST['id']
                object = get_object_or_404(Furniture, pk=id)
                object.delete()
            if 'save' in self.request.POST:
                form = FurnitureForm(self.request.POST)

                if form.is_valid(): # All validation rules pass
                    form.save()
                    form = FurnitureForm()

        selectfloor = Select(choices=floors).render('selectfloor', floor, attrs={'id':'selectfloor'})

        self.template = 'furniture'
        self.kwargs = {'selectfloor': selectfloor, 'form':form}


def edit_device(request):
    if request.method == 'POST':
        if 'id' in request.POST and request.POST['id'] != 'None':
            id = request.POST['id']
            object = get_object_or_404(Device, pk=id)
            if 'delete' in request.POST:
                print 'delete'
                object.delete()
                return HttpResponseRedirect(reverse('desktop.views.settings', kwargs={'type': 'devices'}))

            elif 'save' in request.POST:
                form = DeviceForm(request.POST, instance=object)
                form.fields['code'].widget = object.object.CODE_WIDGET()
                form.fields['action'].widget = object.object.ACTION_WIDGET()

                if form.is_valid(): # All validation rules pass
                    form.save()
                    return HttpResponseRedirect(reverse('desktop.views.settings', kwargs={'type': 'devices'}))

            elif 'sync' in request.POST:
                object.object.action(action='sync')

            form = DeviceForm(instance=object)
            form.fields['code'].widget = object.object.CODE_WIDGET()
            form.fields['action'].widget = object.object.ACTION_WIDGET()
        else:
            type = request.POST['type']
            object = Device(type=type)
            object.object.new()

            if 'add' in request.POST:
                form = DeviceForm(request.POST, instance=object)
            else:
                form = DeviceForm(instance=object)

            form.fields['code'].widget = object.object.CODE_WIDGET()
            form.fields['action'].widget = object.object.ACTION_WIDGET()

            if 'add' in request.POST:
                if form.is_valid(): # All validation rules pass
                    form.save()
                    return HttpResponseRedirect(reverse('desktop.views.settings', kwargs={'type': 'devices'}))

                list = Device.objects.all()
                form = DeviceFormNew()
                return setting(request, settings='devices', devices=list, object=object, form=form)
            else:
                return render(request, 'desktop/settings/devices/device.html', {'object': object, 'form': form, 'add': True})

    else:
        return False

    return render(request, 'desktop/settings/devices/device.html', {'object': object, 'form': form})

def scenarios_settings(request, id=0):
    formset = ScenarioFormSet()
    if request.method == 'POST':
        if 'save' in request.POST:
            formset = ScenarioFormSet(request.POST)
            if formset.is_valid():
                formset.save()
                formset = ScenarioFormSet()

        elif 'edit' in request.POST:
            return render(request, 'desktop/settings/scenarios/scenarios_edit.html', {'formset': formset})

    if id != 0:
        form = ScenarioDeviceFormNew()
        scenariodevices = ScenarioDevice.objects.filter(scenario=id)
        return setting(request, settings='scenarios', formset=formset, scenario=id, form=form, scenariodevices=scenariodevices)
    else:
        return setting(request, settings='scenarios', formset=formset)

def edit_scenario(request):
    if request.method == 'POST' and 'scenario' in request.POST:
        scenarioid = request.POST['scenario']
        scenario = get_object_or_404(Scenario, pk=scenarioid)
        scenariodevices = ScenarioDevice.objects.select_related().filter(scenario=scenarioid)
        if 'add' in request.POST:
            form = ScenarioDeviceFormNew(request.POST)
            if form.is_valid():
                device = form.cleaned_data['device']
                if 'action' in request.POST:
                    action = request.POST['action']
                else:
                    action = 'off'
                newinstance = ScenarioDevice(device=device, scenario=scenario, action=action)
                newinstance.save()
                return HttpResponseRedirect(reverse('desktop.views.scenarios_settings', kwargs={'id': scenarioid}))

        form = ScenarioDeviceFormNew()

        return render(request, 'desktop/settings/scenarios/scenario.html', {'form': form, 'scenario': scenarioid, 'scenariodevices': scenariodevices})

    elif request.method == 'POST' and 'id' in request.POST:
        id = request.POST['id']
        object = get_object_or_404(ScenarioDevice, pk=id)
        form = ScenarioDeviceFormAction(instance=object)
        if 'delete' in request.POST:
            object.delete()
            return HttpResponseRedirect(reverse('desktop.views.scenarios_settings', kwargs={'id': object.scenario.id}))

        elif 'save' in request.POST:
            form = ScenarioDeviceFormAction(request.POST, instance=object)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('desktop.views.scenarios_settings', kwargs={'id': object.scenario.id}))

        return render(request, 'desktop/settings/scenarios/scenariodevice.html', {'form': form, 'object': object})

    else:
        raise Http404('No scenario')

def edit_input(request):
    object = None
    form = None
    add = False
    if request.method == 'POST':
        if 'id' in request.POST:
            id = request.POST['id']
            object = get_object_or_404(Input, pk=id)
            if 'delete' in request.POST:
                print 'delete'
                object.delete()
                return HttpResponseRedirect(reverse('desktop.views.settings', kwargs={'type': 'inputs'}))

            elif 'save' in request.POST:
                postdata = request.POST.copy()
                postdata['action_object'] = postdata['device_scenario']

                form = InputForm(postdata, instance=object)

                if form.is_valid(): # All validation rules pass
                    form.save()
                    return HttpResponseRedirect(reverse('desktop.views.settings', kwargs={'type': 'inputs'}))

            form = InputForm(instance=object)

        else:
            if 'scan' in request.POST:
                input = Input.scan()
                if input is None:
                    return HttpResponse('<input type="button" value="%s" onclick="scan()"/>' % _('Scan'))
                else:
                    object = Input()
                    object.protocol = input.protocol
                    object.data = input.data
                    form = InputForm(instance=object)
                    add = True
            elif 'add' in request.POST:
                postdata = request.POST.copy()
                postdata['device_scenario'] = postdata['action_object']

                object = Input()
                form = InputForm(postdata, instance=object)

                if form.is_valid(): # All validation rules pass
                    form.save()
                    return HttpResponseRedirect(reverse('desktop.views.settings', kwargs={'type': 'inputs'}))
    else:
        return False

    return render(request, 'desktop/settings/inputs/input.html', {'object': object, 'form': form, 'add': add})

def edit_timer(request):
    if request.method == 'POST':
        if 'id' in request.POST:
            id = request.POST['id']
            object = get_object_or_404(Timer, pk=id)
            if 'delete' in request.POST:
                print 'delete'
                object.delete()
                return HttpResponseRedirect(reverse('desktop.views.settings', kwargs={'type': 'timers'}))

            elif 'save' in request.POST:
                postdata = request.POST.copy()
                postdata['action_object'] = postdata['device_scenario']

                form = TimerForm(postdata, instance=object)

                if form.is_valid(): # All validation rules pass
                    form.save()
                    return HttpResponseRedirect(reverse('desktop.views.settings', kwargs={'type': 'timers'}))

            form = TimerForm(instance=object)

        else:
            postdata = request.POST.copy()
            postdata['action_object'] = postdata['device_scenario']

            object = Timer()
            form = TimerForm(postdata, instance=object)

            if form.is_valid(): # All validation rules pass
                form.save()
                return HttpResponseRedirect(reverse('desktop.views.settings', kwargs={'type': 'timers'}))
    else:
        return False

    return render(request, 'desktop/settings/timers/timer.html', {'object': object, 'form': form})

def widget_action(request):
    if request.method == 'POST' and 'device' in request.POST:
        id = request.POST['device']
        device = get_object_or_404(Device, pk=id)

        if 'dim_level' in device.object.SUPPORTED_ACTIONS:
            widget = OnOffDimLevel(device=device)
        else:
            widget = OnOff()
    else:
        raise Http404('No device specified')

    return HttpResponse(widget.render('action', 'off'))