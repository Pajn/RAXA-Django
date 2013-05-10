from django.conf.urls import patterns, url


urlpatterns = patterns('',
                       url(r'^connector/', 'backend.views.connector'),
                       url(r'^input/', 'backend.views.input'),
)
