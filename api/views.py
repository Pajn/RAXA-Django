import json
from django.http import HttpResponse
from backend.models.Connector import Connector
from backend.models.Device import Device
from backend.models.Scenario import Scenario
from backend.models.Room import Floor
from backend.system import updates

API_VERSION = 1
RAXA_VERSION = updates.version()

def respond_with_json(data, errors=None, pretty=False, request=None):
    if not errors: errors = []
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

def serialize_connector(connector):
    output = {
        'id': connector.id,
        'name': connector.name,
        'type': connector.type,
        'code': connector.code,
        }
    return output

def index(request):
    response = {}
    errors = []
    if request.REQUEST.has_key('get'):
        get = request.REQUEST['get'].split(',')
        for data in get:
            if data == 'version':
                response['version'] = version(request, render_json=False)
            elif data == 'devices':
                response['devices'] = devices(request, render_json=False)
            elif data == 'scenarios':
                response['scenarios'] = scenarios(request, render_json=False)
            elif data == 'floors':
                response['floors'] = floors(request, render_json=False)
            elif data == 'connectors':
                response['connectors'] = connectors(request, render_json=False)
            else:
                errors.append('%s is not valid' % data)

    return respond_with_json(response, request=request, errors=errors)

def version(request, render_json = True):
    response = {
        'api': API_VERSION,
        'raxa': RAXA_VERSION,
        }
    if render_json:
        return respond_with_json(response, request=request)
    else:
        return response

def devices(request, render_json = True):
    if request.REQUEST.has_key('room'):
        room = request.REQUEST['room']
        list = Device.objects.filter(room=room)
    else:
        list = Device.objects.all()
    devices = []
    for device in list:
        devices.append(serialize_device(device))
    if render_json:
        return respond_with_json(devices, request=request)
    else:
        return devices

def device(request):
    id = request.REQUEST['id']
    action = request.REQUEST['action']
    device = Device.objects.get(pk=id)
    device.object.action(action=action)
    return respond_with_json('', request=request)

def scenarios(request, render_json = True):
    list = Scenario.objects.all()
    scenarios = []
    for scenario in list:
        scenarios.append(serialize_scenario(scenario))
    if render_json:
        return respond_with_json(scenarios, request=request)
    else:
        return scenarios

def scenario(request):
    id = request.REQUEST['id']
    scenario = Scenario.objects.get(pk=id)
    scenario.execute()
    return respond_with_json('', request=request)

def floors(request, render_json = True):
    list = Floor.objects.all()
    floors = []
    for floor in list:
        floors.append(serialize_floor(floor))
    if render_json:
        return respond_with_json(floors, request=request)
    else:
        return floors

def connectors(request, render_json = True):
    list = Connector.objects.all()
    connectors = []
    for connector in list:
        connectors.append(serialize_connector(connector))
    if render_json:
        return respond_with_json(connectors, request=request)
    else:
        return connectors