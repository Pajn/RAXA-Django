from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('testapp.views',
    url(r'^$', 'index'),
    url(r'^devices/$', 'devices'),
    url(r'^device/(?P<device_id>\d+)/$', 'device'),
)
