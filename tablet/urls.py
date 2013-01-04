from django.conf.urls import patterns, url

urlpatterns = patterns('tablet.views',
    url(r'^$', 'index'),
    url(r'^devices/$', 'devices'),
)
