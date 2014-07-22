# Create your views here.
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext

def index(request):
    return render_to_response('m/index.html', "", context_instance = RequestContext(request))
