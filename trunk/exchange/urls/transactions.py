from django.conf.urls.defaults import *
urlpatterns = patterns('exchange.views',
                       url('^transactions/?$',
                           'transactions',
                           name='transactions'
                          ),
                      )
