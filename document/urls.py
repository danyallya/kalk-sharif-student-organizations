from django.conf.urls import patterns, url

urlpatterns = patterns(
    'document.views',
    url(r'^list/$', 'documents_list', name='documents_list'),
    url(r'^(?P<document_id>\d+)/$', 'document_page', name='document_page'),
    url(r'^send_rate/$', 'send_rate', name='document_send_rate'),
    url(r'^add/$', 'add_document', name='add_document'),

    url(r'^edit/(?P<document_id>\d+)/$', 'edit_document', name='edit_document'),
    url(r'^add_level/(?P<document_id>\d+)/$', 'add_level', name='add_level'),
    url(r'^content/(?P<document_id>\d+)/$', 'doc_content', name='doc_content'),
    url(r'^delete/$', 'delete_level', name='delete_level'),

    url(r'^edit_level/(?P<level_id>\d+)/$', 'edit_level', name='edit_level'),

    url(r'^references/$', 'doc_references', name='doc_references'),

    url(r'^packages/$', 'package_list', name='package_list'),
    url(r'^packages_load/$', 'package_list_load', name='package_list_load'),

    url(r'^send_package/$', 'send_package', name='send_package'),
    url(r'^package/(?P<package_id>\d+)/$', 'package_page', name='package_page'),
    url(r'^get_package/(?P<package_id>\d+)/$', 'package_download', name='package_download'),
    url(r'^package_send_rate/$', 'package_send_rate', name='package_send_rate'),

)
