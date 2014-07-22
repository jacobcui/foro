# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from school.helper import SchoolHelper

def index(request):
    helper = SchoolHelper()
    schools = helper.getAllValid()
    schools = schools[0:50]
    return render_to_response('school/index.html', {'schools': schools}, context_instance = RequestContext(request))
