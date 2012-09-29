from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from bff.vote.admin import register_basic_admin

admin.autodiscover()

class BasicAdmin(AdminSite):
    pass

basic_admin = BasicAdmin('basic')
register_basic_admin(basic_admin)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bff.views.home', name='home'),
    url(r'^', include('bff.vote.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/advanced/', include(admin.site.urls)),
    url(r'^admin/', include(basic_admin.urls)),
)
