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
    url(r'^settings/timers/$', 'inputs_settings'),
    url(r'^settings/timer/$', 'edit_input'),
    url(r'^settings/timers/$', 'timers_settings'),
    url(r'^settings/timer/$', 'edit_timer'),
    url(r'^widgets/action/$', 'widget_action'),
)
