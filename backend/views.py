import json

from django.http import HttpResponse
from django.utils.translation import ugettext as _

from backend.models.Connector import Connector
from backend.models.Input import Input


def respond_with_json(errors=None, pretty=False, request=None):
    if not errors: errors = []
    if request is not None:
        if request.REQUEST.has_key('pretty'):
            pretty = True
    if not errors:
        status = {'status': 'ok', 'errors': errors}
    else:
        status = {'status': 'error', 'errors': errors}
    response = {'status': status}
    if pretty:
        jsons = json.dumps(response, sort_keys=True,
                           indent=4, separators=(',', ': '))
    else:
        jsons = json.dumps(response)
    return HttpResponse(jsons, mimetype='application/json')


def connector(request):
    errors = []
    if request.REQUEST.has_key('type'):
        if request.REQUEST.has_key('code'):
            object = Connector.objects.filter(type=request.REQUEST['type'], code=request.REQUEST['code'])
            if object.__len__() > 0:
                errors.append('AlreadyExists')
            else:
                name = _('New ') + request.REQUEST['type']
                object = Connector(name=name, type=request.REQUEST['type'], code=request.REQUEST['code'])
                object.save()
        else:
            errors.append('NoCode')
    else:
        errors.append('NoType')
    return respond_with_json(errors=errors, request=request)


def input(request):
    errors = []
    if request.REQUEST.has_key('protocol'):
        if request.REQUEST.has_key('data'):
            Input.received(request.REQUEST['protocol'], request.REQUEST['data'])
        else:
            errors.append('NoData')
    else:
        errors.append('NoProtocol')
    return respond_with_json(errors=errors, request=request)