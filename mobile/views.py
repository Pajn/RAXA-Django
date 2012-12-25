from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from backend.models.Device import Device, DeviceFormOld, DeviceFormNew
from backend.models.Scenario import Scenario, ScenarioDevice, ScenarioForm
from backend.models.Room import Room, RoomForm
from backend.models.Connector import Connector, ConnectorForm
from backend.models.Timer import Timer, TimerForm

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

def new_device(request, id):
    if id == '0':
        print 'new'
        object = Device()
    else:
        object = get_object_or_404(Device, pk=id)

    if request.method == 'POST': # If the form has been submitted...
        if 'delete' in request.POST:
            print 'delete'
            object.delete()
            return HttpResponseRedirect(reverse('mobile.views.devices_settings'))

        else:
            form = DeviceFormOld(request.POST, instance=object)
            if form.is_valid(): # All validation rules pass
                form.save()
                return HttpResponseRedirect(reverse('mobile.views.devices_settings'))
    else:
        if id == '0':
            object.id = 0
            form = DeviceFormOld(instance=object)
        else:
            form = DeviceFormNew(instance=object)

def edit_device(request, id):
    object = get_object_or_404(Device, pk=id)

    if request.method == 'POST': # If the form has been submitted...
        if 'delete' in request.POST:
            print 'delete'
            object.delete()
            return HttpResponseRedirect(reverse('mobile.views.devices_settings'))

        else:
            form = DeviceFormOld(request.POST, instance=object)
            form.fields['code'].widget = object.object.CODE_WIDGET()
            form.fields['action'].widget = object.object.ACTION_WIDGET()

            if form.is_valid(): # All validation rules pass
                form.save()
                return HttpResponseRedirect(reverse('mobile.views.devices_settings'))
    else:
        form = DeviceFormOld(instance=object)
        form.fields['code'].widget = object.object.CODE_WIDGET()
        form.fields['action'].widget = object.object.ACTION_WIDGET()

    return render(request, 'mobile/settings/device.html', {'object': object, 'form': form})

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
    list = ScenarioDevice.objects.filter(scenario=id)
    return render(request, 'mobile/settings/scenario_devices.html', {'id': id, 'list': list})

def edit_scenario_device(request, id, scenariodevice):
    if scenariodevice == '0':
        object = ScenarioDevice(scenario=id)
    else:
        object = get_object_or_404(ScenarioDevice, pk=id)
    return render(request, 'mobile/settings/scenario_device.html', {'object': object})

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
    list = Connector.objects.all()
    return render(request, 'mobile/settings/connectors.html', {'list': list})

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
    list = Room.objects.all()
    return render(request, 'mobile/settings/rooms.html', {'list': list})


def timers_settings(request):
    list = Timer.objects.all()
    return render(request, 'mobile/settings/timers.html', {'list': list})