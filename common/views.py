from django.shortcuts import render
from common.models.Furniture import Furniture
from common.models.Plan import Plan

def overlay(request, floor=1):
    edit_rooms = False

    if request.method == 'POST':
        if 'floor' in request.POST:
            floor = request.POST['floor']
        if 'edit_rooms' in request.POST:
            edit_rooms = True

    rooms = Plan.objects.filter(floor=floor)
    furnitures = Furniture.objects.filter(floor=floor)
    radious=10
    return render(request, 'common/floor.svg', {'rooms':rooms, 'furnitures':furnitures, 'radious':radious, 'edit_rooms':edit_rooms})