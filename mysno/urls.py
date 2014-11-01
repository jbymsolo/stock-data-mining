from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysno.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','mysno.views.first_page'),
    url(r'^west/',include('west.urls')),
    url(r'^media/(?P<path>.*)', 'django.views.static.serve', {'document_root': 'D:/mysno/media'}),
    
)
