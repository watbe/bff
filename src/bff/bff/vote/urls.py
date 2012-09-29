from django.conf.urls import patterns, include, url

urlpatterns = patterns('bff.vote.views',
	url(r'^index.php/$', 'index'),
)
