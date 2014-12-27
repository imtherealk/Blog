from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()
urlpatterns = patterns('',
    url(r'^$', 'blog.views.root'),
    url(r'^blog/$', 'blog.views.index'),
    url(r'^blog/page/(?P<page>[-]?\d+)/$', 'blog.views.index'),
    url(r'^blog/entry/(?P<entry_id>\d+)/$', 'blog.views.read'),
    url(r'^blog/entry/(?P<entry_id>\d+)/delete/$', 'blog.views.delete_post'),
    url(r'^blog/write/$', 'blog.views.write_form'),
    url(r'^blog/add/post/$', 'blog.views.add_post'),
    url(r'^blog/add/comment/$', 'blog.views.add_comment'),
    url(r'^blog/get_comments/(?P<entry_id>\d+)/$', 'blog.views.get_comments'),
    url(r'^blog/login/$', 'blog.views.login_view'),
    url(r'^blog/login_page/$', 'blog.views.login_form'),
    url(r'^blog/logout/$', 'blog.views.logout_view'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.ROOT_PATH + '/media'}),
)
