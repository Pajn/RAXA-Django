from automation.views import Programs, Program, Automation
from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^settings/automation/$', Automation.as_view()),
                       url(r'^settings/automation/programs/$', Programs.as_view(), name='automation_programs'),
                       url(r'^settings/automation/program/(?P<id>\d+)/$',  Program.as_view(), name='automation_program'),
                       )