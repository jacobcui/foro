from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from cloudchoice.models import Vendor
## CloudChoice:
urlpatterns = patterns('cloudchoice.views',
                       url(r'^vendors/$', 'list_vendors' ),
                       url(r'^products/$', 'list_products' ),
                       url(r'^$', 'index'),
)
