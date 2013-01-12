from django.conf.urls import patterns, url

urlpatterns = patterns('desktop.views',
    url(r'^$', 'index'),
    url(r'^devices/$', 'devices'),
    url(r'^settings/$', 'settings'),
    url(r'^settings/devices/$', 'devices_settings'),
    url(r'^settings/device/$', 'edit_device'),
    url(r'^settings/scenarios/$', 'scenarios_settings'),
    url(r'^settings/scenario/$', 'edit_scenario'),
    url(r'^settings/scenarios/(?P<id>\d+)/$', 'scenarios_settings'),
    url(r'^settings/inputs/$', 'inputs_settings'),
    url(r'^settings/input/$', 'edit_input'),
    url(r'^settings/timers/$', 'timers_settings'),
    url(r'^settings/timer/$', 'edit_timer'),
    url(r'^settings/system/$', 'system_settings'),
    url(r'^widgets/action/$', 'widget_action'),
)
