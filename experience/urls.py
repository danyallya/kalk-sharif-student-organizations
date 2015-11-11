from django.conf.urls import patterns, url

urlpatterns = patterns(
    'experience.views',
    url(r'^list/$', 'experiences_list', name='experiences_list'),
    url(r'^list_load/$', 'experiences_list_load', name='experiences_list_load'),
    url(r'^(?P<experience_id>\d+)/$', 'experience_page', name='experience_page'),
    url(r'^experience_page/(?P<experience_id>\d+)/$', 'experience_page', name='experience_page_old'),

    url(r'^send_image/$', 'send_image', name='experience_send_image'),
    url(r'^send_rate/$', 'send_rate', name='experience_send_rate'),
    url(r'^add/$', 'add_experience', name='add_experience'),
)
