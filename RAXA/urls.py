from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns

urlpatterns = patterns('',
                       url(r'^api/', include('api.urls')),
                       url(r'^backend/', include('backend.urls')),
)

urlpatterns += i18n_patterns('',
                             url(r'^', include('desktop.urls')),
                             url(r'^mobile/', include('mobile.urls')),
                             url(r'^common/', include('common.urls')),
                             url(r'^tablet/', include('tablet.urls')),
)
