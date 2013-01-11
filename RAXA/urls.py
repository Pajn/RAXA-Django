from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('desktop.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^mobile/', include('mobile.urls')),
    url(r'^common/', include('common.urls')),
    url(r'^tablet/', include('tablet.urls')),
    url(r'^backend/', include('backend.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
