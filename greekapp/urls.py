from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'nt.views.index', name='index'),
    url(r'^book/(?P<book>[a-zA-Z0-9]+)/(?P<chapter>[0-9]+)/(?P<verse>[0-9]+)/$',
        'nt.views.verse', name='verse'),
)
