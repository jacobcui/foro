# Create your views here.
from django.core import serializers
from django.http import HttpResponse, HttpRequest
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from django.core import serializers
from django.conf import settings
from django import forms
from django.core.exceptions import ObjectDoesNotExist

def index(request):

    if settings.DEBUG:
        javascripts = ["underscore.js", "backbone.js", "three.min.js", "CSS3DRenderer.js"]
    else:
        javascripts = ["underscore-min.js", "backbone-min.js", "three.min.js"]

    javascripts.append("vi/index.js")
    css = ["vi/style.css"];

    dataToTemplate = {
        'title': 'Virtual Inspection',
        'javascripts': javascripts,
        'stylesheets': css,
    }

    return render_to_response('vi/index.html', dataToTemplate, context_instance = RequestContext(request))
