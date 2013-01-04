from django.shortcuts import render

def overlay(request, floor):
    return render(request, 'common/floor%s.svg' % floor)