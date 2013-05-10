from django.http import Http404
from django.shortcuts import render, get_object_or_404
from backend.models.Device import Device
from backend.models.Room import Room, Floor
from backend.models.Scenario import Scenario
import common.views


def index(request):
    floors = Floor.objects.all()
    scenarios = Scenario.objects.all()
    percent = (99 - scenarios.__len__()) / scenarios.__len__()
    return render(request, 'tablet/index.html', {'scenarios': scenarios, 'floors': floors, 'percent': percent})


def login(request):
    return common.views.login(request)


def devices(request):
    if request.REQUEST.has_key('room'):
        room = request.REQUEST['room']
        room = get_object_or_404(Room, pk=room)
        list = Device.objects.filter(room=room.id)
    else:
        raise Http404('No room specified')
    return render(request, 'tablet/devices.html', {'list': list, 'room': room})