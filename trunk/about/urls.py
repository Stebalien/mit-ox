from django.conf.urls.defaults import *
urlpatterns = patterns('about.views',
                       url('^/?$',
                           'about',
                           name='about'
                          ),
                       url('^contact/?$',
                           'contact',
                           name='contact'
                          ),
                       url('^faq/?$',
                           'faq',
                           name='faq'
                          )
                      )
