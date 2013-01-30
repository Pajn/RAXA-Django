from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from backend.io import connector
from backend.models.Device import Device, DeviceForm, DeviceFormNew
from backend.models.Device import supported_types as device_supported_types
from backend.models.Scenario import Scenario, ScenarioDevice, ScenarioForm, ScenarioDeviceForm, ScenarioDeviceFormNew
from backend.models.Room import Room, RoomForm
from backend.models.Connector import Connector, ConnectorForm
from backend.models.Input import Input, InputForm, InputFormNew
from backend.models.Timer import Timer, TimerFormNew, TimerForm
from backend.widgets.DeviceScenario import DeviceScenarioHidden

def index(request):
    return render(request, 'mobile/index.html')

def devices(request, room=False):
    if not room:
        list = Device.objects.all()
    else:
        list = Device.objects.filter(room=room)
    return render(request, 'mobile/devices.html', {'list': list, 'room': room})

def device(request, id, action):
    device = Device.objects.get(pk=id)
    device.object.action(action=action)
    return HttpResponseRedirect(reverse('mobile.views.devices'))

def scenarios(request):
    list = Scenario.objects.all()
    return render(request, 'mobile/scenarios.html', {'list': list})

def scenario(request, id):
    scenario = Scenario.objects.get(pk=id)
    scenario.execute()
    return HttpResponseRedirect(reverse('mobile.views.scenarios'))

def rooms(request):
    list = Room.objects.all()
    return render(request, 'mobile/rooms.html', {'list': list})

def settings(request):
    return render(request, 'mobile/settings.html')

def devices_settings(request):
    list = Device.objects.all()
    return render(request, 'mobile/settings/devices.html', {'list': list})

def new_device(request):
    if request.method == 'POST': # If the form has been submitted...
        form = DeviceFormNew(request.POST)
        form.fields['type'].choices = device_supported_types()
        if form.is_valid(): # All validation rules pass
            type = form.cleaned_data['type']
            return HttpResponseRedirect(reverse('mobile.views.edit_device', kwargs={'type': type,}))
    else:
        form = DeviceFormNew()
        form.fields['type'].choices = device_supported_types()

    return render(request, 'mobile/settings/device_new.html', {'object': object, 'form': form})

def edit_device(request, id=0, type=None):
    if not type:
        object = get_object_or_404(Device, pk=id)
    else:
        object = Device(type=type)
        object.object.new()

    if request.method == 'POST': # If the form has been submitted...
        if 'delete' in request.POST:
            print 'delete'
            object.delete()
            return HttpResponseRedirect(reverse('mobile.views.devices_settings'))

        else:
            form = DeviceForm(request.POST, instance=object)
            form.fields['code'].widget = object.object.CODE_WIDGET()
            form.fields['action'].widget = object.object.ACTION_WIDGET()

            if form.is_valid(): # All validation rules pass
                form.save()
                return HttpResponseRedirect(reverse('mobile.views.devices_settings'))
    else:
        form = DeviceForm(instance=object)
        form.fields['code'].widget = object.object.CODE_WIDGET()
        form.fields['action'].widget = object.object.ACTION_WIDGET()

    return render(request, 'mobile/settings/device.html', {'object': object, 'form': form, 'type': type})

def scenarios_settings(request):
    list = Scenario.objects.all()
    return render(request, 'mobile/settings/scenarios.html', {'list': list})

def edit_scenario(request, id):
    if id == '0':
        print 'new'
        object = Scenario()
    else:
        object = get_object_or_404(Scenario, pk=id)

    if request.method == 'POST': # If the form has been submitted...
        if 'delete' in request.POST:
            print 'delete'
            object.delete()
            return HttpResponseRedirect(reverse('mobile.views.scenarios_settings'))

        else:
            form = ScenarioForm(request.POST, instance=object)
            if form.is_valid(): # All validation rules pass
                form.save()
                return HttpResponseRedirect(reverse('mobile.views.scenarios_settings'))
    else:
        if id == '0':
            object.id = 0
        form = ScenarioForm(instance=object)

    return render(request, 'mobile/settings/scenario.html', {'object': object, 'form': form})

def edit_scenario_devices(request, id):
    object = get_object_or_404(Scenario, pk=id)
    list = ScenarioDevice.objects.filter(scenario=id)
    return render(request, 'mobile/settings/scenario_devices.html', {'object': object, 'list': list})

def edit_scenario_device(request, scenario, scenariodevice):
    scenario = get_object_or_404(Scenario, pk=scenario)
    submit = 'delete'
    if request.method == 'POST': # If the form has been submitted...
        if 'new' in request.POST:
            # First step submitted
            form = ScenarioDeviceFormNew(request.POST)
            if form.is_valid(): # All validation rules pass
                device = form.cleaned_data['device']
                object = ScenarioDevice(device=device, scenario=scenario)
                form = ScenarioDeviceForm(instance=object)
                form.fields['device_new'].widget.attrs['value'] = device.id
                submit = 'save'
                return render(request, 'mobile/settings/scenario_device.html', {'form': form, 'scenario': scenario, 'scenariodevice': scenariodevice, 'submit': submit})
        elif 'delete' in request.POST:
            # Delete requested
            object = get_object_or_404(ScenarioDevice, pk=scenariodevice)
            object.delete()
            return HttpResponseRedirect(reverse('mobile.views.edit_scenario_devices', kwargs={'id': scenario.id,}))
        else:
            postdata = request.POST.copy()
            # second step submitted
            if scenariodevice == '0':
                postdata['device'] = postdata['device_new']
                form = ScenarioDeviceFormNew(postdata)
                device = get_object_or_404(Device, pk=form._raw_value('device'))
                object = ScenarioDevice(device=device, scenario=scenario)
                submit = 'save'
            else:
                object = get_object_or_404(ScenarioDevice, pk=scenariodevice)
            form = ScenarioDeviceForm(postdata, instance=object)
            if form.is_valid(): # All validation rules pass
                form.save()
                return HttpResponseRedirect(reverse('mobile.views.edit_scenario_devices', kwargs={'id': scenario.id,}))
    else:
        if scenariodevice == '0':
            form = ScenarioDeviceFormNew()
            submit = 'next'
        else:
            object = get_object_or_404(ScenarioDevice, pk=scenariodevice)
            form = ScenarioDeviceForm(instance=object)

    return render(request, 'mobile/settings/scenario_device.html', {'form': form, 'scenario': scenario, 'scenariodevice': scenariodevice, 'submit': submit})

def rooms_settings(request):
    list = Room.objects.all()
    return render(request, 'mobile/settings/rooms.html', {'list': list})

def edit_room(request, id):
    object = get_object_or_404(Room, pk=id)
    if request.method == 'POST': # If the form has been submitted...
        form = RoomForm(request.POST, instance=object)
        if form.is_valid(): # All validation rules pass
            form.save()
            return HttpResponseRedirect(reverse('mobile.views.rooms_settings'))
    else:
        form = RoomForm(instance=object)

    return render(request, 'mobile/settings/room.html', {'object': object, 'form': form})


def connectors_settings(request):
    list = Connector.objects.all()
    return render(request, 'mobile/settings/connectors.html', {'list': list})


def scan_connectors(request):
    connector.scan_connectors()
    return HttpResponseRedirect(reverse('mobile.views.connectors_settings'))

def edit_connector(request, id):
    object = get_object_or_404(Connector, pk=id)
    if request.method == 'POST': # If the form has been submitted...
        if 'delete' in request.POST:
            print 'delete'
            object.delete()
            return HttpResponseRedirect(reverse('mobile.views.connectors_settings'))

        else:
            form = ConnectorForm(request.POST, instance=object)
            if form.is_valid(): # All validation rules pass
                form.save()
                return HttpResponseRedirect(reverse('mobile.views.connectors_settings'))
    else:
        form = ConnectorForm(instance=object)

    return render(request, 'mobile/settings/connector.html', {'object': object, 'form': form})

def inputs_settings(request):
    list = Input.objects.exclude(pk=0)
    return render(request, 'mobile/settings/inputs.html', {'list': list})

def scan_input(request):
    input = Input.scan()
    if input is None:
        return HttpResponseRedirect(reverse('mobile.views.inputs_settings'))
    else:
        return HttpResponseRedirect(reverse('mobile.views.edit_input', kwargs={'id': 0,}))

def edit_input(request, id):
    submit = 'delete'
    if request.method == 'POST': # If the form has been submitted...
        if 'new' in request.POST:
            # First step submitted
            form = InputFormNew(request.POST)
            if form.is_valid(): # All validation rules pass
                action_object = form._raw_value('device_scenario')
                object = Input(action_object=action_object)
                form = InputForm(instance=object)
                form.fields['device_scenario'].widget = DeviceScenarioHidden(value=object.action_object)
                submit = 'save'
                return render(request, 'mobile/settings/input.html', {'form': form, 'id': id, 'submit': submit})
        elif 'delete' in request.POST:
            # Delete requested
            object = get_object_or_404(Input, pk=id)
            object.delete()
            return HttpResponseRedirect(reverse('mobile.views.inputs_settings'))
        else:
            # second step
            postdata = request.POST.copy()
            postdata['action_object'] = postdata['device_scenario']
            object = get_object_or_404(Input, pk=id)
            if id == '0':
                form = InputForm(request.POST)
                action_object = form._raw_value('device_scenario')
                object.action_object = action_object
                submit = 'save'
            form = InputForm(postdata, instance=object)
            if form.is_valid(): # All validation rules pass
                form.save()
                return HttpResponseRedirect(reverse('mobile.views.inputs_settings'))
    else:
        if id == '0':
            form = InputFormNew()
            submit = 'next'
        else:
            object = get_object_or_404(Input, pk=id)
            form = InputForm(instance=object)

    return render(request, 'mobile/settings/input.html', {'form': form, 'id': id, 'submit': submit})

def timers_settings(request):
    list = Timer.objects.all()
    return render(request, 'mobile/settings/timers.html', {'list': list})

def edit_timer(request, id):
    submit = 'delete'
    if request.method == 'POST': # If the form has been submitted...
        if 'new' in request.POST:
            # First step submitted
            form = TimerFormNew(request.POST)
            if form.is_valid(): # All validation rules pass
                action_object = form._raw_value('device_scenario')
                object = Timer(action_object=action_object)
                form = TimerForm(instance=object)
                form.fields['device_scenario'].widget = DeviceScenarioHidden(value=object.action_object)
                submit = 'save'
                return render(request, 'mobile/settings/timer.html', {'form': form, 'id': id, 'submit': submit})
        elif 'delete' in request.POST:
            # Delete requested
            object = get_object_or_404(Timer, pk=id)
            object.delete()
            return HttpResponseRedirect(reverse('mobile.views.timers_settings'))
        else:
            # second step
            postdata = request.POST.copy()
            postdata['action_object'] = postdata['device_scenario']
            if id == '0':
                form = TimerForm(request.POST)
                action_object = form._raw_value('device_scenario')
                object = Timer(action_object=action_object)
                submit = 'save'
            else:
                object = get_object_or_404(Timer, pk=id)
            form = TimerForm(postdata, instance=object)
            if form.is_valid(): # All validation rules pass
                form.save()
                return HttpResponseRedirect(reverse('mobile.views.timers_settings'))
    else:
        if id == '0':
            form = TimerFormNew()
            submit = 'next'
        else:
            object = get_object_or_404(Timer, pk=id)
            form = TimerForm(instance=object)

    return render(request, 'mobile/settings/timer.html', {'form': form, 'id': id, 'submit': submit})