from django.shortcuts import render
from common.models.Furniture import Furniture

def overlay(request, floor=0):
    furnitures = Furniture.objects.filter(floor=floor)
    radious=10
    floor = 'common/individuals/floor%s.svg' % floor
    return render(request, 'common/floor.svg', {'furnitures':furnitures, 'radious':radious, 'floor':floor})