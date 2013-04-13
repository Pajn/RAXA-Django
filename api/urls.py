from django.conf.urls import patterns, url

urlpatterns = patterns('api.views',
    url(r'^$', 'index'),
    url(r'^login/$', 'login'),
    url(r'^version/$', 'version'),
    url(r'^(?P<view>devices)/$', 'view'),
    url(r'^(?P<view>device)/$', 'view'),
    url(r'^(?P<view>scenarios)/$', 'view'),
    url(r'^(?P<view>scenario)/$', 'view'),
    url(r'^(?P<view>floors)/$', 'view'),
    url(r'^(?P<view>connectors)/$', 'view'),
)
