from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from backend.authorization import get_user
from backend.models.User import LoginForm
from common.models import Temp
from common.models.Furniture import Furniture
from common.models.Plan import Plan
from RAXA.local_settings import SVG_ATTR


def login(request, template='common/login.html', **kwargs):
    if request.method == 'POST':
        print request.POST['password']
        if get_user().check_password(request.POST['password']):
            request.session['auth'] = 1
            return HttpResponseRedirect(request.session.get('url', default=reverse('desktop.views.index')))
    loginform = LoginForm()
    kwargs['loginform'] = loginform
    return render(request, template, kwargs)


def overlay(request, floor=1):
    edit_rooms = False

    if request.method == 'POST':
        if 'floor' in request.POST:
            floor = request.POST['floor']
        if 'edit_rooms' in request.POST:
            edit_rooms = True

    rooms = Plan.objects.select_related('room__id').filter(floor=floor)
    furnitures = Furniture.objects.select_related('device').filter(floor=floor)
    temps = Temp.objects.select_related('thermometer').filter(floor=floor)
    radious = 10
    return render(request, 'common/floor.svg',
                  {'SVG_ATTR': SVG_ATTR[int(floor)], 'rooms': rooms, 'furnitures': furnitures, 'temps': temps,
                   'radious': radious, 'edit_rooms': edit_rooms})