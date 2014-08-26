from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
	url(r'^$', 'usermanagement.views.social_account_login_or_sign_up', name='social-account-login-or-sign-up'),
    url(r'^social-accounts-invite-friends/$', 'Social.views.social_accounts_invite_friends', name='social_accounts_invite_friends'),
    url(r'^request-connection/$', 'Social.views.request_connection', name="request_connection"),
    url(r'^friend-requests/$', 'Social.views.friend_requests', name="friend_requests"), # view all friend requests to user
    url(r'^send-message/$', 'Social.views.send_message', name="send_message"),
    url(r'^message-inbox/$', 'Social.views.message_inbox', name="message_inbox"),
    url(r'^mark-seen/$', 'Social.views.mark_seen', name="mark_seen"), #url to change status from unseen to seen when user clicks on message
    url(r'^view-all-messages-to-and-from-member/$', 'Social.views.view_all_messages_to_and_from_member', name="view_all_messages_to_and_from_member"),
    url(r'^about-us/$', 'Social.views.about_us'),
    url(r'^search_location', 'Social.views.search_location', name='search_location'),

	#url(r'^my-profile/$', 'Social.views.my_profile', name='my-profile'),
	url(r'^refresh-new-messages/$', 'Social.views.refresh_new_messages_div', name="refresh_new_messages_div"),

	url(r'^my-connections/$', 'Social.views.my_connections', name="my_connections"),
	url(r'^pending-connections/$', 'Social.views.pending_connections', name="pending_connections"),
	url(r'^view-others-profile/$', 'Social.views.view_others_profile', name="view_others_profile"),
	url(r'^send-message-popup/$', 'Social.views.send_message_popup', name="send_message_popup"),
	url(r'^edit-profile-details/$', 'Social.views.edit_profile_details', name="edit_profile_details"),
	url(r'^delete-skill/', 'Social.views.delete_skill',name='delete_skill'),
	url(r'^add-name/', 'Social.views.add_name', name="add_name"),


)
