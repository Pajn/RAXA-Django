from django.conf.urls import patterns, url

urlpatterns = patterns('common.views',
    url(r'^login/$', 'login'),
    url(r'^overlay/$', 'overlay'),
    url(r'^overlay/(?P<floor>\d+)/$', 'overlay'),
)
