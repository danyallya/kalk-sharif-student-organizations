from django.conf.urls import patterns, url

urlpatterns = patterns('utils.ajax.views',
                       url(r'^validationEngine/$', 'validationEngine', name='ajax_validationEngine'),
                       url(r'^select2/$', 'select2', name='select2'),
                       url(r'^tag_search/$', 'tag_search', name='tag_search'),

                       url(r'^uni_search/$', 'uni_search', name='uni_search'),

                       )
