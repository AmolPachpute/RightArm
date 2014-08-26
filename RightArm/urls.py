from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'RightArm.views.home', name='home'),
    # url(r'^RightArm/', include('RightArm.foo.urls')),

    url(r'^login/$', 'usermanagement.views.user_login', name='user_login'),
    url(r'^user-profile/$', 'usermanagement.views.user_profile', name='user_profile'),
    url(r'^accounts/', include('registration.urls')),
    url(r'^$', 'usermanagement.views.home', name='home'),
    url(r'^accounts/profile/', include('Social.urls'), name='profile'),
    url(r'^projects/', include('Projects.urls')),
    url(r'^social/', include('Social.urls')),
    url(r'^configure/(?P<key>.*)/$', 'usermanagement.views.configure', name='configure'),
    url(r'^manage_configure/(?P<key>.*)/(?P<task>(:?add|:?edit|:?delete|:?active|:?viewmore))/$', 'usermanagement.views.manage_configure', name='configure'),
    url(r'^problems/', include('Problems.urls')),
    url(r'^logout/', 'usermanagement.views.user_logout', name='user_logout'),
    url(r'^linked_in/', include('linked_integration.urls')),
    url(r'^google/login/$', 'django_openid_auth.views.login_begin', name='openid-login'),
    url(r'^google/login-complete/$', 'django_openid_auth.views.login_complete', name='openid-complete'),
    url(r'^check-user/$', 'usermanagement.views.check_user', name='check_user'),
    url(r'^search-results/$', 'Social.views.search_results', name='search_results'),
    url(r'',include('social_auth.urls')),

    url(r'^faq/', 'anonymous.views.faq',name='faq'),
    url(r'^contact-us/', 'anonymous.views.contactus',name='contact_us'),
    url(r'^about-us/', 'anonymous.views.about_us',name='about_us'),
    url(r'^edit-profile-photo/$', 'Social.views.edit_profile_photo', name='edit_profile_photo'),
    url(r'^terms-condition/', 'anonymous.views.terms_condition',name='terms_condition'),
    url(r'^policy/', 'anonymous.views.policy',name='policy'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', \
                    {'document_root': 'static'}),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^discussions/', include('forums.urls', namespace='forums')),
    url(r'^forum-comment/$', 'forums.views.forum_comment', name = 'forum_comment'),
    url(r'^create-topic/$', 'forums.views.create_topic', name = 'create_topic'),
    url(r'^topic-post/$', 'forums.views.topic_post', name = 'topic_post'),

    url(r'^msg-to_search/$', 'Social.views.msg_to_search', name="msg_to_search"),

    # Facebook Login Url:

    url(r'^facebook_login/$', 'usermanagement.views.facebook_login'),
    url(r'^facebook_login_success/$', 'usermanagement.views.facebook_login_success'),
    url(r'^facebook_javascript_login_sucess/$', 'usermanagement.views.facebook_javascript_login_sucess'),

    # Country Search URL:

    url(r'^country-search-results/$', 'usermanagement.views.search_function'),
    url(r'^join-rightarm/$', 'usermanagement.views.join_function'),
	url(r'^update-notifications-div/$', 'Social.views.update_notifications_div', name='update_notifications_div'),

    # Conversation URL:

    url(r'^get-conversation/$', 'Social.views.get_conversation', name = 'get-conversation'),
    url(r'^change-password/$', 'usermanagement.views.change_password', name = 'change-password'),

	url(r'^contacts/', include("django_contact_importer.contacts.urls")),

	url(r'^invite-friends/$', 'Social.views.invite_friends', name='invite_friends'),


)
