from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'west.views.jieguo'),
    url(r'^jieguo/', 'west.views.jieguo'),
     url(r'^jieguo/media/(?P<path>.*)', 'django.views.static.serve', {'document_root': 'D:/mysno/media'}),
)
