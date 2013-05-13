from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from RAXA.settings import MEDIA_URL, MEDIA_ROOT

urlpatterns = patterns('',
                       url(r'^api/', include('api.urls')),
                       url(r'^backend/', include('backend.urls')),
) + static(MEDIA_URL, document_root=MEDIA_ROOT)

urlpatterns += i18n_patterns('',
                             url(r'^', include('desktop.urls')),
                             url(r'^mobile/', include('mobile.urls')),
                             url(r'^common/', include('common.urls')),
                             url(r'^tablet/', include('tablet.urls')),
)
