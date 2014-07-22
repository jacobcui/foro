# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse

from django.template import Context, loader
from django.template import RequestContext

def index(request):
    return render_to_response('builder/index.html', context_instance = RequestContext(request))
