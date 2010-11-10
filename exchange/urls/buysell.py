from django.conf.urls.defaults import *

urlpatterns = patterns('exchange.views',
                       url(r'^/?$',
                           'categories',
                           name='categories'
                          ),
                       url(r'^search/?$',
                           'search',
                           name='search'
                          ),
                      )
