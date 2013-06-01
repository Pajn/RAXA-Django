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
from django.conf.urls import patterns, url
from desktop.views import DesktopView, DevicesView, SettingsView, DevicesSettingsView, DeviceSettingsView,\
    EditScenariosSettingsView, ScenarioSettingsView, ScenarioDeviceSettingsView, InputsSettingsView, InputSettingsView,\
    TimersSettingsView, TimerSettingsView, ThermometersSettingsView, FurnitureSettingsView, SystemSettingsView,\
    ConnectorsSettingsView, NetworkSettingsView, SecuritySettingsView, ThemesSettingsView, RoomSettingsView,\
    RoomsSettingsView, FloorsSettingsView, PlanSettingsView

urlpatterns = patterns('',
                       url(r'^$', DesktopView.as_view(), name='index'),
                       url(r'^login/$', 'common.views.login', name='login'),
                       url(r'^devices/$', DevicesView.as_view(), name='devices'),
                       url(r'^devices/(?P<room>\d+)/$', DevicesView.as_view(), name='devices'),
                       url(r'^settings/$', SettingsView.as_view(), name='settings'),
                       url(r'^settings/devices/$', DevicesSettingsView.as_view(), name='settings_devices'),
                       url(r'^settings/device/$', DeviceSettingsView.as_view(), name='settings_device'),
                       url(r'^settings/scenarios/$', EditScenariosSettingsView.as_view(), name='settings_scenarios'),
                       url(r'^settings/scenario/(?P<id>\d+)/$', ScenarioSettingsView.as_view(), name='settings_scenario'),
                       url(r'^settings/scenario_device/$', ScenarioDeviceSettingsView.as_view(), name='settings_scenariodevice'),
                       url(r'^settings/inputs/$', InputsSettingsView.as_view(), name='settings_inputs'),
                       url(r'^settings/input/$', InputSettingsView.as_view(), name='settings_input'),
                       url(r'^settings/timers/$', TimersSettingsView.as_view(), name='settings_timers'),
                       url(r'^settings/timer/$', TimerSettingsView.as_view(), name='settings_timer'),
                       url(r'^settings/thermometers/$', ThermometersSettingsView.as_view(), name='settings_thermometers'),
                       url(r'^settings/furniture/$', FurnitureSettingsView.as_view(), name='settings_furniture'),
                       url(r'^settings/system/$', SystemSettingsView.as_view(), name='settings_system'),
                       url(r'^settings/system/connectors/$', ConnectorsSettingsView.as_view(), name='system_connectors'),
                       url(r'^settings/system/network/$', NetworkSettingsView.as_view(), name='system_network'),
                       url(r'^settings/system/security/$', SecuritySettingsView.as_view(), name='system_security'),
                       url(r'^settings/system/themes/$', ThemesSettingsView.as_view(), name='system_themes'),
                       url(r'^settings/room/$', RoomSettingsView.as_view(), name='settings_room'),
                       url(r'^settings/room/rooms/$', RoomsSettingsView.as_view(), name='room_rooms'),
                       url(r'^settings/room/floors/$', FloorsSettingsView.as_view(), name='room_floors'),
                       url(r'^settings/room/plan/$', PlanSettingsView.as_view(), name='room_plan'),
                       url(r'^widgets/action/$', 'desktop.views.widget_action', name='widget_action'),
)