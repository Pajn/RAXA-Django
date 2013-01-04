from django.conf.urls import patterns, url

urlpatterns = patterns('desktop.views',
    url(r'^$', 'index'),
    url(r'^devices/$', 'devices'),
)
