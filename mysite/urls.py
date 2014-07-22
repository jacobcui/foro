from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from polls.models import Poll
from crm.models import Applicant, Contact
# Uncomment the next two lines to enable the admin:
from django.contrib import admin


admin.autodiscover()

handler404 = 'mysite.views.http_404'
handler500 = 'mysite.views.http_500'
handler505 = 'mysite.views.http_505'


#urlpatterns = patterns('polls.views',
                       # Examples:
                       #    url(r'^$', 'mysite.views.home', name='home'),
                       # url(r'^mysite/', include('mysite.foo.urls')),
                       
                       # Uncomment the admin/doc line below to enable admin documentation:
                           # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       
                       # Uncomment the next line to enable the admin:

#                       url(r'^polls/$', 'index'),
#                       url(r'^polls/(?P<poll_id>\d+)/$', 'detail'),
#                       url(r'^polls/(?P<poll_id>\d+)/results/$', 'results'),
#                       url(r'^polls/(?P<poll_id>\d+)/vote/$', 'vote'),
#                       )



urlpatterns = patterns('crm.views', 
                       url(r'^crm$', 'index'),
                       url(r'^crm/(?P<applicant_id>\d+)$', 'detail'),

                       url(r'^crm/list$',
                           ListView.as_view( queryset = Applicant.objects.order_by('index'),
                                             context_object_name = 'applicant_list',
                                             template_name='crm/list.html'),
                           name='index' ),
                       
                       )

urlpatterns += patterns('mysite.views', 
                        url(r'^listpictures', 'listpictures'),
                        url(r'^admin/', include(admin.site.urls)),
                        url(r'^/$', 'index'),
                        url(r'^$', 'index'),
                        url(r'^terms[/]$', 'terms'),
                        url(r'^privacy[/]$', 'privacy'),
                        url(r'^profile$', 'profile'),
                        url(r'^about$', 'about'),
                        url(r'^contact$', 'contact'),
                        url(r'^get-startted[/]$', 'getstartted'),
                        url(r'^apps/get/(?P<appname>\w+)[/]$', 'getApplication'),
                        url(r'^get/(?P<resource>.*)/(?P<username>\w+)/(?P<textid>\w+)/(?P<index>\w+)/(?P<options>\w+)[/]$', 'getresource'),
                        url(r'^signup[/]$', 'signup'),
                        url(r'^NQ4bch2.html$', 'cert'),
                       )

urlpatterns += patterns('',
                        url(r'^login[/]$', 'django.contrib.auth.views.login', {'template_name': 'login.html', 'extra_context': {'next': '/profile'}}),
                        url(r'^logout[/]$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html', 'extra_context':{'next': '/login'}}), 
                        )

urlpatterns += patterns('builder.views',
                        url(r'^builder$', 'index'),

                        )

urlpatterns += patterns('school.views',
                        url(r'^school[/]$', 'index'),
                        )

urlpatterns += patterns('ce.views',
                        url(r'^ce[/]$', 'index'),
                        url(r'^ce/upload[/]$', 'upload'),
                        url(r'^ce/contact[/]$', 'contact'),
                        url(r'^ce/thanks[/]$', 'thanks'),
                        
                        )

urlpatterns += patterns('report.views',
                        url(r'^report[/]$', 'index'),
                        url(r'^report/test[/]$', 'test'),
                        url(r'^report/gencsrf[/]$', 'gencsrf'),
                        url(r'^report/generate[/]$', 'generate'),
                        url(r'^report/getplan/(?P<planid>\w+)[/]$', 'getPlan'),
                        
                    )

urlpatterns += patterns('file.views',
                        url(r'^file/(?P<userid>\d+)[/](?P<filename>.*)$', 'getfile'),

    )

urlpatterns += patterns('m.views',
                        url(r'^m[/]$', 'index')
                    )


## Adding url patterns for other apps
urlpatterns += patterns('cloudchoice.views',
    url(r'^cloudchoice/', include('cloudchoice.urls')),
)

urlpatterns += patterns('vi.views',
    url(r'^vi/', include('vi.urls')),
)

#urlpatterns += patterns('',
#                       url(r'^$',
#                           ListView.as_view( queryset = Poll.objects.order_by('-pub_date')[:5],
#                                             context_object_name = 'latest_poll_list',
#                                             template_name='polls/index.html'),
#                           name='index' ),
#                       url(r'^(?P<pk>\d+)/$',
#                           DetailView.as_view( model = Poll,
#                                               template_name = 'polls/detail.html'),
#                           name='detail' ),
#                       url(r'^(?P<pk>\d+)/results/$',
#                           DetailView.as_view( model = Poll,
#                                               template_name = 'polls/results.html'),
#                           name = 'results'),
#                       url(r'^(?P<poll_id>\d+)/vote/$', 'polls.views.vote', 
#                           name='vote'),
#        )
