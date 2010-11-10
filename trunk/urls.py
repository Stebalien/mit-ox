from django.conf.urls.defaults import *
from settings import MEDIA_ROOT

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from djapian import load_indexes
load_indexes()

urlpatterns = patterns('',
    # Homepage
    (r'^$|index\.[a-zA-Z0-9]{1,4}', 'homepage.views.index'),
    # Exchange
    (r'^(?P<mode>(buy|sell))/', include('exchange.urls.buysell')),
    (r'^add/', include('exchange.urls.add')),
    (r'^transactions/', include('exchange.urls.transactions')),
    # Accounts
    (r'^accounts/', include('accounts.urls')),
    # About
    (r'^about/', include('about.urls')),
    # Images (THIS IS TEMPORARY, FIXME) **!!&&*!@*(##(*$&@#(*$&(&@*(@*&#&(
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
             {'document_root': MEDIA_ROOT}),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
