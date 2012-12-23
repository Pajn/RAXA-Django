from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from backend.models.Device import Device
from backend.models.Scenario import Scenario
from backend.models.Room import Room

def index(request):
    return render_to_response('mobile/index.html')

def devices(request, room=False):
    if not room:
        device_list = Device.objects.all()
    else:
        device_list = Device.objects.filter(room=room)
    return render_to_response('mobile/devices.html', {'device_list': device_list})

def device(request, device, action):
    device = Device.objects.get(pk=device)
    device.object.action(action=action)
    return HttpResponseRedirect(reverse('mobile.views.devices'))

def edit_device(request, device):
    p = get_object_or_404(Device, pk=device)
    return render_to_response('mobile/device.html', {'device': p})

def scenarios(request):
    scenario_list = Scenario.objects.all()
    return render_to_response('mobile/scenarios.html', {'scenario_list': scenario_list})

def scenario(request, scenario):
    scenario = Scenario.objects.get(pk=scenario)
    scenario.execute()
    return HttpResponseRedirect(reverse('mobile.views.scenarios'))

def rooms(request):
    room_list = Room.objects.all()
    return render_to_response('mobile/rooms.html', {'room_list': room_list})

def settings(request):
    return render_to_response('mobile/settings.html')