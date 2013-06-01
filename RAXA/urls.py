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
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from RAXA.settings import MEDIA_URL, MEDIA_ROOT, INSTALLED_PLUGINS

urls = (url(r'^api/', include('api.urls')),
        url(r'^backend/', include('backend.urls')),)

i18n_urls = (url(r'^', include('desktop.urls')),
             url(r'^mobile/', include('mobile.urls')),
             url(r'^common/', include('common.urls')),
             url(r'^tablet/', include('tablet.urls')),)

for plugin in INSTALLED_PLUGINS:
    try:
        urls += (url(r'^', include('%s.urls' % plugin)),)
    except ImportError:
        pass
    try:
        i18n_urls += (url(r'^', include('%s.i18n_urls' % plugin)),)
    except ImportError:
        pass

urlpatterns = patterns('', *urls) + static(MEDIA_URL, document_root=MEDIA_ROOT)

urlpatterns += i18n_patterns('', *i18n_urls)