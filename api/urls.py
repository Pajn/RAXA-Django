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
