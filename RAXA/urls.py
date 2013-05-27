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