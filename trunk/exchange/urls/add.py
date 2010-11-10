from django.conf.urls.defaults import *

urlpatterns = patterns('exchange.views',
                       url(r'^/?$',
                           'additem',
                           name='additem_choose_category'
                          ),
                       url(r'^(?P<mode>\w+)/?$',
                           'additem',
                           name='additem_choose_category'
                          ),
                       url(r'^(?P<mode>(\w+))/(?P<category>\w+)/?$',
                           'additem',
                           name='additem'
                          ),
                      )
