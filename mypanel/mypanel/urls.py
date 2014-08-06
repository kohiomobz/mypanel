from django.conf.urls import patterns, include, url

#  Import mypanel views
from mypanel.views import hello, index, track, query

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mypanel.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    ('^hello/$', hello),
    ('^$', index),
    ('^track', track),
    ('^query', query),
)
