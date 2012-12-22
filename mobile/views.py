from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from backend.models.Device import Device
from backend.models.Scenario import Scenario

def index(request):
    return render_to_response('mobile/index.html')

def devices(request):
    device_list = Device.objects.all()
    return render_to_response('mobile/devices.html', {'device_list': device_list})

def device(request, device_id, action):
    device = Device.objects.get(pk=device_id)
    device.object.action(action=action)
    return HttpResponseRedirect(reverse('mobile.views.devices'))

def edit_device(request, device_id):
    p = get_object_or_404(Device, pk=device_id)
    return render_to_response('mobile/device.html', {'device': p})

def scenarios(request):
    scenario_list = Device.objects.all()
    return render_to_response('mobile/scenarios.html', {'scenario_list': scenario_list})

def scenario(request, scenario_id):
    scenario = Scenario.objects.get(pk=scenario_id)
    scenario.execute()
    return HttpResponseRedirect(reverse('mobile.views.scenarios'))

def rooms(request):
    room_list = Device.objects.all()
    return render_to_response('mobile/devices.html', {'room_list': room_list})

def settings(request):
    return render_to_response('mobile/settings.html')