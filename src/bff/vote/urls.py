from django.conf.urls import patterns, include, url

urlpatterns = patterns('bff.vote.views',
	url(r'^$', 'login'),
	url(r'^vote/(?P<room>\d+)/$', 'vote', name='vote'),
)
