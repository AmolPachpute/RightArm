from django.conf.urls import patterns, include, url



urlpatterns = patterns('',
    # Examples:
    url(r'^details/$', 'Projects.views.project_details'),
    url(r'^project-list/$', 'Projects.views.list_all_projects'),
    url(r'^project-category/$', 'Projects.views.project_category'),
    url(r'^add-project/$', 'Projects.views.add_project'),
    url(r'^edit-project/$', 'Projects.views.edit_project'),
    url(r'^delete-project/$', 'Projects.views.delete_project'),
    
)