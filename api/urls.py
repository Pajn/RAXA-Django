from django.conf.urls import patterns, url

urlpatterns = patterns('api.views',
    url(r'^$', 'index'),
    url(r'^version/$', 'version'),
    url(r'^devices/$', 'devices'),
    url(r'^device/$', 'device'),
    url(r'^scenarios/$', 'scenarios'),
    url(r'^scenario/$', 'scenario'),
    url(r'^floors/$', 'floors'),
    url(r'^connectors/$', 'connectors'),
)
