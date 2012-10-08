from django.conf.urls import patterns, include, url

urlpatterns = patterns('bff.vote.views',
	url(r'^$', 'login'),
	url(r'^vote/$', 'vote', name='vote'),
	url(r'^stats/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'stats', name='stats'),
)
