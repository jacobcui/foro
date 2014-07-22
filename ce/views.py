# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from ce.forms import ContactForm

from school.helper import SchoolHelper

def index(request):
    return render_to_response('ce/index.html', {'text': 'Hello'}, context_instance = RequestContext(request))

def thanks(request):
    return render_to_response('ce/thanks.html', {}, context_instance = RequestContext(request))

def upload(request):
    return render_to_response('ce/upload.html', {'text': 'ce->upload', 'request': request}, context_instance = RequestContext(request))

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/ce/thanks')
    else:
        form = ContactForm()

    return render_to_response('ce/contact.html', {'form': form}, context_instance = RequestContext(request))
#    return render(request, 'ce/contact.html', {'form':form})
