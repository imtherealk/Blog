from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()
urlpatterns = patterns('',
    url(r'^blog/$', 'blog.views.index'),
    url(r'^blog/page/(?P<page>[-]?\d+)/$', 'blog.views.index'),
    url(r'^blog/entry/(?P<entry_id>\d+)/$', 'blog.views.read'),
    url(r'^blog/write/$', 'blog.views.write_form'),
    url(r'^blog/add/post/$', 'blog.views.add_post'),
    url(r'^blog/add/comment/$', 'blog.views.add_comment'),
    url(r'^admin/', include(admin.site.urls)),
)
