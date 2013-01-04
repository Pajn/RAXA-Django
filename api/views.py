import json
from django.shortcuts import render
from django.http import HttpResponse
from backend.models.Device import Device
from backend.models.Scenario import Scenario
from backend.models.Room import Floor

API_VERSION = 2
RAXA_VERSION = 2

def respond_with_json(data, errors=[], pretty=False, request=None):
    if request is not None:
        if request.REQUEST.has_key('pretty'):
            pretty = True
    if not errors:
        status = {'status': 'ok', 'errors': errors}
    else:
        status = {'status': 'error', 'errors': errors}
    response = {'response': data, 'status': status}
    if pretty:
        jsons = json.dumps(response, sort_keys=True,
                           indent=4, separators=(',', ': '))
    else:
        jsons = json.dumps(response)
    return HttpResponse(jsons, mimetype='application/json')

def serialize_device(device):
    output = {
        'id': device.id,
        'name': device.name,
        'type': device.type,
        'code': device.code,
        'connector': device.connector.id,
        'room': device.room.id,
        'floor': device.room.floor.id,
        'order': device.order,
        'action': device.action,
        'status': device.status,
        'supported_actions': device.object.SUPPORTED_ACTIONS.keys(),
        'connector_type': device.object.CONNECTOR_TYPE
    }
    return output

def serialize_scenario(scenario):
    output = {
        'id': scenario.id,
        'name': scenario.name,
        'is_hidden': scenario.is_hidden,
        'order': scenario.order,
    }
    return output

def serialize_room(room):
    output = {
        'id': room.id,
        'name': room.name,
        }
    return output

def serialize_floor(floor):
    rooms = []
    for room in floor.room_set.all():
        rooms.append(serialize_room(room))
    output = {
        'id': floor.id,
        'name': floor.name,
        'rooms': rooms,
        }
    return output

def index(request):
    return render(request, 'mobile/index.html')

def version(request):
    response = {
        'api': API_VERSION,
        'raxa': RAXA_VERSION,
        }
    return respond_with_json(response, request=request)

def devices(request, room=False):
    if not room:
        list = Device.objects.all()
    else:
        list = Device.objects.filter(room=room)
    devices = []
    for device in list:
        devices.append(serialize_device(device))
    return respond_with_json(devices, request=request)

def device(request, id, action):
    device = Device.objects.get(pk=id)
    device.object.action(action=action)
    return respond_with_json('', request=request)

def scenarios(request):
    list = Scenario.objects.all()
    scenarios = []
    for scenario in list:
        scenarios.append(serialize_scenario(scenario))
    return respond_with_json(scenarios, request=request)

def scenario(request, id):
    scenario = Scenario.objects.get(pk=id)
    scenario.execute()
    return respond_with_json('', request=request)

def floors(request):
    list = Floor.objects.all()
    floors = []
    for floor in list:
        floors.append(serialize_floor(floor))
    return respond_with_json(floors, request=request)