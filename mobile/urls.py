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

urlpatterns = patterns('mobile.views',
                       url(r'^$', 'index'),
                       url(r'^login/$', 'login'),
                       url(r'^devices/$', 'devices'),
                       url(r'^devices/(?P<room>\d+)/$', 'devices'),
                       url(r'^device/(?P<id>\d+)/cmd/(?P<action>[a-zA-Z0-9_]+)/$', 'device'),
                       url(r'^scenarios/$', 'scenarios'),
                       url(r'^scenario/(?P<id>\d+)/$', 'scenario'),
                       url(r'^rooms/$', 'rooms'),
                       url(r'^settings/$', 'settings'),
                       url(r'^settings/devices/$', 'devices_settings'),
                       url(r'^settings/device/new/$', 'new_device'),
                       url(r'^settings/device/(?P<id>\d+)/$', 'edit_device'),
                       url(r'^settings/device/(?P<type>[a-zA-Z0-9_]+)/$', 'edit_device'),
                       url(r'^settings/scenarios/$', 'scenarios_settings'),
                       url(r'^settings/scenario/(?P<id>\d+)/$', 'edit_scenario'),
                       url(r'^settings/scenario/(?P<id>\d+)/devices$', 'edit_scenario_devices'),
                       url(r'^settings/scenario/(?P<scenario>\d+)/device/(?P<scenariodevice>\d+)$',
                           'edit_scenario_device'),
                       url(r'^settings/rooms/$', 'rooms_settings'),
                       url(r'^settings/room/(?P<id>\d+)/$', 'edit_room'),
                       url(r'^settings/connectors/$', 'connectors_settings'),
                       url(r'^settings/connector/scan/$', 'scan_connectors'),
                       url(r'^settings/connector/(?P<id>\d+)/$', 'edit_connector'),
                       url(r'^settings/inputs/$', 'inputs_settings'),
                       url(r'^settings/inputs/scan$', 'scan_input'),
                       url(r'^settings/inputs/(?P<id>\d+)/$', 'edit_input'),
                       url(r'^settings/timers/$', 'timers_settings'),
                       url(r'^settings/timer/(?P<id>\d+)/$', 'edit_timer'),
                       url(r'^settings/device/(?P<device>\d+)/$', 'edit_device'),
)
