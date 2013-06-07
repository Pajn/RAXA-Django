from django.conf.urls import url, patterns
from automation.views import Programs, Program, Drawingboard, LogicBlockDelete, LogicLink, FunctionSettings

urlpatterns = patterns('',
    url(r'^settings/automation/$', Programs.as_view(), name='automation_programs'),
    url(r'^settings/automation/(?P<id>\d+)/$', Program.as_view(), name='automation_program'),
    url(r'^settings/automation/(?P<id>\d+)/drawingboard.svg$', Drawingboard.as_view(), name='automation_drawingboard'),
    url(r'^automation/logic_block_delete/$', LogicBlockDelete.as_view(), name='automation_logic_block_delete'),
    url(r'^automation/logic_link/$', LogicLink.as_view(), name='automation_logic_link'),
    url(r'^automation/automation_function_settings/$', FunctionSettings.as_view(), name='automation_function_settings'),
)