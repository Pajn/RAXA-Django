from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from backend.models.Device import Device

def index(request):
    return render_to_response('testapp/index.html')

def devices(request):
    device_list = Device.objects.all()
    return render_to_response('testapp/devices.html', {'device_list': device_list})

def device(request, device_id, cmd):
    Device.objects.get(pk=device_id).object.action(cmd)
    #p = get_object_or_404(Device, pk=device_id)
    #return render_to_response('testapp/device.html', {'device': p})
    return HttpResponseRedirect(reverse('mobile.views.devices'))