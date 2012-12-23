from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('mobile.views',
    url(r'^$', 'index'),
    url(r'^devices/$', 'devices'),
    url(r'^devices/(?P<room>\d+)/$', 'devices'),
    url(r'^device/(?P<device>\d+)/cmd/(?P<action>[a-zA-Z0-9_]+)/$', 'device'),
    url(r'^device/(?P<device>\d+)/$', 'edit_device'),
    url(r'^scenarios/$', 'scenarios'),
    url(r'^scenario/(?P<scenario>\d+)/$', 'scenario'),
    url(r'^rooms/$', 'rooms'),
    url(r'^settings/$', 'settings'),
)
