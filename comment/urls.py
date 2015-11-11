from django.conf.urls import patterns, url

urlpatterns = patterns(
    'comment.views',
    url(r'^send/(?P<content_type_id>\d+)/$', 'send_comment', name='send_comment'),

    url(r'^show/(?P<content_type_id>\d+)/$', 'show_comments', name='show_comments'),

    url(r'^count/(?P<content_type_id>\d+)/$', 'comments_count', name='comments_count'),
)
