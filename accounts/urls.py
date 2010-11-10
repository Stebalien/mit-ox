from django.conf.urls.defaults import *

urlpatterns = patterns('accounts.views',
                       url('^profile/$',
                           'profile',
                           name='profile'
                          ),
                      )

urlpatterns += patterns('',
                        url(r'^login/$',
                            'django.contrib.auth.views.login',
                            {'template_name': 'accounts/login.html'},
                            name='login',
                        ),
                        url(r'logout/$',
                            'django.contrib.auth.views.logout',
                            {'next_page': '/'},
                            name='logout',
                        )
                       )


