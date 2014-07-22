from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from cloudchoice.models import Vendor
## CloudChoice:
urlpatterns = patterns('vi.views',
                       url(r'^$', 'index'),
)
