from django import forms
from backend.models import Floor


def floor_select(selected=None):
    floors = []
    for floor in Floor.objects.all():
        floors.append((floor.id, floor.name))
    return forms.Select(choices=floors).render('selectfloor', selected, attrs={'id': 'selectfloor'})