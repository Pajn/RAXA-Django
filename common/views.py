from django.shortcuts import render
from common.models import Temp
from common.models.Furniture import Furniture
from common.models.Plan import Plan
from RAXA.local_settings import SVG_ATTR

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
    radious=10
    return render(request, 'common/floor.svg', {'SVG_ATTR': SVG_ATTR[int(floor)], 'rooms':rooms, 'furnitures':furnitures, 'temps':temps, 'radious':radious, 'edit_rooms':edit_rooms})