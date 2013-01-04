from django.conf.urls import patterns, url

urlpatterns = patterns('api.views',
    url(r'^$', 'index'),
    url(r'^version/$', 'version'),
    url(r'^devices/$', 'devices'),
    url(r'^device/(?P<id>\d+)/(?P<action>[a-zA-Z0-9_]+)/$', 'device'),
    url(r'^scenarios/$', 'scenarios'),
    url(r'^scenario/(?P<id>\d+)/$', 'scenario'),
    url(r'^floors/$', 'floors'),
)
