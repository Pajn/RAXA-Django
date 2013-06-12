'''
Copyright (C) 2013 Rasmus Eneman <rasmus@eneman.eu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from backend.models.Device import Device
from backend.models.Room import Room, Floor
from backend.models.Scenario import Scenario
import common.views


def index(request, **kwargs):
    floors = Floor.objects.all()
    scenarios = Scenario.objects.all()
    percent = (99 - scenarios.__len__()) / scenarios.__len__()
    kwargs['theme'] = request.session['theme']
    kwargs['scenarios'] = scenarios
    kwargs['floors'] = floors
    kwargs['percent'] = percent
    return render(request, 'tablet/index.html', kwargs)


def login(request):
    return common.views.login(request)


def devices(request):
    if 'room' in request.REQUEST:
        room = request.REQUEST['room']
        room = get_object_or_404(Room, pk=room)
        list = Device.objects.filter(room=room.id)
    else:
        raise Http404('No room specified')
    return render(request, 'tablet/devices.html', {'list': list, 'room': room})