from django.conf.urls import patterns, url
from views import Settings

urlpatterns = patterns('desktop.views',
    url(r'^$', 'index'),
    url(r'^devices/$', 'devices'),
    url(r'^settings/$', 'settings'),
    url(r'^settings/$', 'settings_index'),
    url(r'^settings/device/$', 'edit_device'),
    url(r'^settings/scenarios/$', 'scenarios_settings'),
    url(r'^settings/scenario/$', 'edit_scenario'),
    url(r'^settings/scenarios/(?P<id>\d+)/$', 'scenarios_settings'),
    url(r'^settings/input/$', 'edit_input'),
    url(r'^settings/timer/$', 'edit_timer'),
    url(r'^settings/(?P<type>[a-z]+)/$', 'settings'),
    url(r'^widgets/action/$', 'widget_action'),
)
