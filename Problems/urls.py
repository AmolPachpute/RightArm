from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^challenge/$', 'Problems.views.manage_challange', name='manage_challange'),
    #url(r'^giver/$', 'Problems.views.manage_giver', name='manage_giver'),
)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'static'}),
)
