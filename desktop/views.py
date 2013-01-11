from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from backend.models import InputForm
from backend.models.Device import Device, DeviceForm
from backend.models.Input import Input
from backend.models.Room import Room, Floor
from backend.models.Scenario import Scenario, ScenarioFormSet, ScenarioDevice, ScenarioDeviceFormNew, ScenarioDeviceFormAction
from backend.models.Timer import Timer, TimerForm

def index(request, template='desktop/index.html', **kwargs):
    floors = Floor.objects.all()
    scenarios = Scenario.objects.all()
    percent = (98-scenarios.__len__()) / (scenarios.__len__()+1)
    kwargs['scenarios'] = scenarios
    kwargs['floors'] = floors
    kwargs['percent'] = percent
    return render(request, template, kwargs)

def devices(request):
    if request.REQUEST.has_key('room'):
        room = request.REQUEST['room']
        room = get_object_or_404(Room, pk=room)
        list = Device.objects.filter(room=room.id)
    else:
        raise Http404('No room specified')
    return render(request, 'desktop/devices.html', {'list': list, 'room': room})

def settings(request):
    if request.method == 'POST':
        type = request.POST['type']
        if type == 'Devices':
            list = Device.objects.all()
            form = DeviceForm()
            return render(request, 'desktop/settings/devices.html', {'devices': list, 'form': form})
        elif type == 'Scenarios':
            scenarios = Scenario.objects.all()
            formset = ScenarioFormSet()
            return render(request, 'desktop/settings/scenarios.html', {'scenarios': scenarios, 'formset': formset})
        elif type == 'Inputs':
            list = Input.objects.all()
            form = InputForm()
            return render(request, 'desktop/settings/inputs.html', {'inputs': list, 'form': form})
        elif type == 'Timers':
            list = Timer.objects.all()
            form = TimerForm()
            return render(request, 'desktop/settings/timers.html', {'timers': list, 'form': form})
    else:
        return index(request, template='desktop/settings.html')

def devices_settings(request):
    list = Device.objects.all()
    form = DeviceForm()
    return index(request, template='desktop/settings/devices_full.html', devices=list, form=form)

def edit_device(request):
    if request.method == 'POST':
        if 'id' in request.POST:
            id = request.POST['id']
            object = get_object_or_404(Device, pk=id)
            if 'delete' in request.POST:
                print 'delete'
                object.delete()
                return HttpResponseRedirect(reverse('desktop.views.devices_settings'))

            elif 'save' in request.POST:
                form = DeviceForm(request.POST, instance=object)
                form.fields['code'].widget = object.object.CODE_WIDGET()
                form.fields['action'].widget = object.object.ACTION_WIDGET()

                if form.is_valid(): # All validation rules pass
                    form.save()
                    return HttpResponseRedirect(reverse('desktop.views.devices_settings'))

            form = DeviceForm(instance=object)
            form.fields['code'].widget = object.object.CODE_WIDGET()
            form.fields['action'].widget = object.object.ACTION_WIDGET()
        else:
            type = request.POST['type']

            object = Device(type=type)
            object.object.new()
            print object.code
            print object.action

            postdata = request.POST.copy()
            if postdata['code'] == '':
                postdata['code'] = object.code
            if postdata['action'] == '':
                postdata['action'] = object.action

            form = DeviceForm(postdata, instance=object)
            form.fields['code'].widget = object.object.CODE_WIDGET()
            form.fields['action'].widget = object.object.ACTION_WIDGET()

            if form.is_valid(): # All validation rules pass
                form.save()
                return HttpResponseRedirect(reverse('desktop.views.devices_settings'))

            list = Device.objects.all()
            return index(request, 'desktop/settings/devices_full.html', devices=list, object=object, form=form)

    else:
        return False

    return render(request, 'desktop/settings/device.html', {'object': object, 'form': form})

def scenarios_settings(request, id=0):
    formset = ScenarioFormSet()
    if request.method == 'POST':
        if 'save' in request.POST:
            formset = ScenarioFormSet(request.POST)
            if formset.is_valid():
                formset.save()
                formset = ScenarioFormSet()

        elif 'edit' in request.POST:
            return render(request, 'desktop/settings/scenarios_edit.html', {'formset': formset})

    if id != 0:
        form = ScenarioDeviceFormNew()
        scenariodevices = ScenarioDevice.objects.filter(scenario=id)
        return index(request, template='desktop/settings/scenarios_full.html', formset=formset, scenario=id, form=form, scenariodevices=scenariodevices)
    else:
        return index(request, template='desktop/settings/scenarios_full.html', formset=formset)

def edit_scenario(request):
    if request.method == 'POST' and 'scenario' in request.POST:
        scenarioid = request.POST['scenario']
        scenario = get_object_or_404(Scenario, pk=scenarioid)
        scenariodevices = ScenarioDevice.objects.filter(scenario=scenarioid)
        if 'add' in request.POST:
            form = ScenarioDeviceFormNew(request.POST)
            if form.is_valid():
                device = form.cleaned_data['device']
                newinstance = ScenarioDevice(device=device, scenario=scenario, action='off')
                newinstance.save()
                return HttpResponseRedirect(reverse('desktop.views.scenarios_settings', kwargs={'id': scenarioid}))

        form = ScenarioDeviceFormNew()

        return render(request, 'desktop/settings/scenario.html', {'form': form, 'scenario': scenarioid, 'scenariodevices': scenariodevices})

    elif request.method == 'POST' and 'id' in request.POST:
        id = request.POST['id']
        object = get_object_or_404(ScenarioDevice, pk=id)
        form = ScenarioDeviceFormAction(instance=object)
        if 'delete' in request.POST:
            object.delete()
            return HttpResponseRedirect(reverse('desktop.views.scenarios_settings', kwargs={'id': object.scenario.id}))

        elif 'save' in request.POST:
            form = ScenarioDeviceFormAction(request.POST, instance=object)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('desktop.views.scenarios_settings', kwargs={'id': object.scenario.id}))

        return render(request, 'desktop/settings/scenariodevice.html', {'form': form, 'object': object})

    else:
        raise Http404('No scenario')

def inputs_settings(request):
    list = Input.objects.all()
    form = InputForm()
    return index(request, template='desktop/settings/inputs_full.html', inputs=list, form=form)

def edit_input(request):
    if request.method == 'POST':
        if 'id' in request.POST:
            id = request.POST['id']
            object = get_object_or_404(Timer, pk=id)
            if 'delete' in request.POST:
                print 'delete'
                object.delete()
                return HttpResponseRedirect(reverse('desktop.views.timers_settings'))

            elif 'save' in request.POST:
                postdata = request.POST.copy()
                postdata['action_object'] = postdata['device_scenario']

                form = TimerForm(postdata, instance=object)

                if form.is_valid(): # All validation rules pass
                    form.save()
                    return HttpResponseRedirect(reverse('desktop.views.timers_settings'))

            form = TimerForm(instance=object)

        else:
            postdata = request.POST.copy()
            postdata['action_object'] = postdata['device_scenario']

            object = Timer()
            form = TimerForm(postdata, instance=object)

            if form.is_valid(): # All validation rules pass
                form.save()
                return HttpResponseRedirect(reverse('desktop.views.timers_settings'))
    else:
        return False

    return render(request, 'desktop/settings/timer.html', {'object': object, 'form': form})

def timers_settings(request):
    list = Timer.objects.all()
    form = TimerForm()
    return index(request, template='desktop/settings/timers_full.html', timers=list, form=form)

def edit_timer(request):
    if request.method == 'POST':
        if 'id' in request.POST:
            id = request.POST['id']
            object = get_object_or_404(Timer, pk=id)
            if 'delete' in request.POST:
                print 'delete'
                object.delete()
                return HttpResponseRedirect(reverse('desktop.views.timers_settings'))

            elif 'save' in request.POST:
                postdata = request.POST.copy()
                postdata['action_object'] = postdata['device_scenario']

                form = TimerForm(postdata, instance=object)

                if form.is_valid(): # All validation rules pass
                    form.save()
                    return HttpResponseRedirect(reverse('desktop.views.timers_settings'))

            form = TimerForm(instance=object)

        else:
            postdata = request.POST.copy()
            postdata['action_object'] = postdata['device_scenario']

            object = Timer()
            form = TimerForm(postdata, instance=object)

            if form.is_valid(): # All validation rules pass
                form.save()
                return HttpResponseRedirect(reverse('desktop.views.timers_settings'))
    else:
        return False

    return render(request, 'desktop/settings/timer.html', {'object': object, 'form': form})