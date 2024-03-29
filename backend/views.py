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
import json

from django.http import HttpResponse
from django.utils.translation import ugettext as _
from backend.io.connector import supported_types

from backend.models.Connector import Connector
from backend.models.Input import Input


def respond_with_json(errors=None, pretty=False, request=None):
    if not errors: errors = []
    if request is not None:
        if 'pretty'in request.REQUEST:
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
    if 'type' in request.REQUEST:
        if 'code' in request.REQUEST:
            if 'version' in request.REQUEST:
                if request.REQUEST['type'] in supported_types():
                    objects = Connector.objects.filter(type=request.REQUEST['type'], code=request.REQUEST['code'])
                    if objects.__len__() > 0:
                        if objects.__len__() == 1:
                            object = objects[0]
                            if object.version == request.REQUEST['version']:
                                errors.append('AlreadyExists')
                            else:
                                object.version = request.REQUEST['version']
                                object.save()
                        else:
                            objects.delete()
                            name = _('New ') + request.REQUEST['type']
                            object = Connector(name=name, type=request.REQUEST['type'], code=request.REQUEST['code'],
                                               version=request.REQUEST['version'])
                            object.save()
                    else:
                        name = _('New ') + request.REQUEST['type']
                        object = Connector(name=name, type=request.REQUEST['type'], code=request.REQUEST['code'],
                                           version=request.REQUEST['version'])
                        object.save()
                else:
                    errors.append('TypeNotSupported')
            else:
                errors.append('NoVersion')
        else:
            errors.append('NoCode')
    else:
        errors.append('NoType')
    return respond_with_json(errors=errors, request=request)


def input(request):
    errors = []
    if 'protocol' in request.REQUEST:
        if 'data' in request.REQUEST:
            Input.received(request.REQUEST['protocol'], request.REQUEST['data'])
        else:
            errors.append('NoData')
    else:
        errors.append('NoProtocol')
    return respond_with_json(errors=errors, request=request)