from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hashtag_miner.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'miner.views.index'),
    url(r'^contact', 'miner.views.contact'),
    url(r'^about', 'miner.views.about'),
    url(r'^redirect/', 'miner.views.authorize'),
    url(r'^admin/', include(admin.site.urls)),
)
