import json
from django.http import HttpResponse
from backend.authorization import get_user
from backend.models.Connector import Connector
from backend.models.Device import Device
from backend.models.Scenario import Scenario
from backend.models.Room import Floor
from backend.system import updates

API_VERSION = 2
RAXA_VERSION = updates.version()

def respond_with_json(data, errors=None, pretty=False, request=None):
    if not errors: errors = []
    if request is not None:
        if 'pretty' in request.REQUEST:
            pretty = True
    if not errors:
        status = {'status': 'ok', 'errors': errors}
    else:
        status = {'status': 'error', 'errors': errors}
    status['version'], err = version()
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
        'room': device.room.id,
        'floor': device.room.floor.id,
        'order': device.order,
        'action': device.action,
        'status': device.status,
        'supported_actions': device.object.SUPPORTED_ACTIONS.keys(),
        'connector_type': device.object.CONNECTOR_TYPE
    }
    if device.connector is not None:
        output['connector'] = device.connector.id
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

def view(request, view='login', render_json=True):
    if render_json:
        response, errors = globals()[view](request)
        return respond_with_json(response, request=request, errors=errors)
    else:
        return globals()[view](request), []

def view_auth(request, view='index', render_json=True):
    if request.session.get('auth', default=0) == -1:
        errors = ['Unauthorized:' + view]
        if render_json:
            return respond_with_json({}, request=request, errors=errors)
        else:
            return None, errors
    else:
        if render_json:
            response, errors = globals()[view](request)
            return respond_with_json(response, request=request, errors=errors)
        else:
            return globals()[view](request)

def index(request):
    response = {}
    errors = []
    if request.REQUEST.has_key('get'):
        get = request.REQUEST['get'].split(',')
        for data in get:
            if data in ['version']:
                response[data], error = view(request, view=data, render_json=False)
                if error.__len__() > 0:
                    response.pop(data)
                    errors.extend(error)
            elif data in ['devices', 'scenarios', 'floors', 'connectors']:
                response[data], error = view_auth(request, view=data, render_json=False)
                if error.__len__() > 0:
                    response.pop(data)
                    errors.extend(error)
            else:
                errors.append('NotValid:' + data)

    return respond_with_json(response, request=request, errors=errors)

def login(request):
    response = {}
    errors = []
    if 'password' in request.REQUEST:
        user = get_user()
        if user.check_password(request.REQUEST['password']):
            response['key'] = user.api_key
        else:
            errors.append('Bad Password')
    else:
        errors.append('NotSet:password')

    return respond_with_json(response, request=request, errors=errors)

def version(*args):
    response = {
        'api': API_VERSION,
        'raxa': RAXA_VERSION,
        }
    return response, []

def devices(request):
    if 'room' in request.REQUEST:
        room = request.REQUEST['room']
        query = Device.objects.filter(room=room)
    else:
        query = Device.objects.all()
    devices = []
    for device in query:
        devices.append(serialize_device(device))
    return devices, []

def device(request):
    try:
        pk = request.REQUEST['id']
    except KeyError:
        return '', ['NotSet:id']
    try:
        action = request.REQUEST['action']
    except KeyError:
        return '', ['NotSet:action']
    try:
        device = Device.objects.get(pk=pk)
        try:
            device.object.action(**request.REQUEST)
        except KeyError:
            return '', ['ActionNotSupported:' + action]
        return '', []
    except Device.DoesNotExist:
        return '', ['DoesNotExist:Device']

def scenarios(*args):
    query = Scenario.objects.all()
    scenarios = []
    for scenario in query:
        scenarios.append(serialize_scenario(scenario))
    return scenarios, []

def scenario(request):
    try:
        pk = request.REQUEST['id']
    except KeyError:
        return '', ['NotSet:id']
    try:
        scenario = Scenario.objects.get(pk=pk)
        scenario.execute()
        return '', []
    except Scenario.DoesNotExist:
        return '', ['DoesNotExist:Scenario']

def floors(*args):
    query = Floor.objects.all()
    floors = []
    for floor in query:
        floors.append(serialize_floor(floor))
    return floors, []

def connectors(*args):
    query = Connector.objects.all()
    connectors = []
    for connector in query:
        connectors.append(serialize_connector(connector))
    return connectors, []