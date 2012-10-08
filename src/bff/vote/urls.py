from django.conf.urls import patterns, url

urlpatterns = patterns('bff.vote.views',
	url(r'^$', 'login'),
	url(r'^vote/$', 'vote', name='vote'),
	url(r'^stats/(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d+)/$', 'stats', name='stats'),
	url(r'^stats/$', 'stats_index', name='stats_index'),
	url(r'^stats/search/$', 'stats_search', name='search'),
	url(r'^stats/page/(?P<page>\d+)/$', 'stats_index_page', name='stats_index_page'),
)
