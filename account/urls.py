from django.conf.urls import patterns, url

urlpatterns = patterns(
    'account.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),

    url(r'^signup/$', 'signup', name='signup'),

    url(r'^forget/$', 'forget', name='forget'),
    url(r'^change_pass/$', 'change_pass', name='change_pass'),

    url(r'^$', 'account_page', name='account_page'),
    url(r'^edit_account/$', 'edit_account', name='edit_account'),
    url(r'^upgrade/$', 'upgrade', name='upgrade'),

    url(r'^search/$', 'search', name='search'),

    url(r'^seen_notification/(?P<notification_id>\d+)/$', 'seen_notification', name='seen_notification'),

)
