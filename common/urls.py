from django.conf.urls import patterns, url

urlpatterns = patterns('common.views',
    url(r'^overlay/(?P<floor>\d+)/$', 'overlay'),
)
