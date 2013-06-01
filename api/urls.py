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

urlpatterns = patterns('api.views',
                       url(r'^$', 'index'),
                       url(r'^login/$', 'login'),
                       url(r'^(?P<view>version)/$', 'view'),
                       url(r'^(?P<view>devices)/$', 'view_auth'),
                       url(r'^(?P<view>device)/$', 'view_auth'),
                       url(r'^(?P<view>scenarios)/$', 'view_auth'),
                       url(r'^(?P<view>scenario)/$', 'view_auth'),
                       url(r'^(?P<view>floors)/$', 'view_auth'),
                       url(r'^(?P<view>connectors)/$', 'view_auth'),
)
