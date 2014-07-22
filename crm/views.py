# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, loader
from django.template import RequestContext

from crm.models import Applicant, Contact

def index(request):
    if request.method == 'GET':
        # <view logic>
        return HttpResponse('result')


def detail(request, applicant_id):
    if request.method == 'GET':
        # <view logic>
        applicant = get_object_or_404(Applicant, pk=applicant_id)
        return render_to_response('crm/detail.html', {'applicant': applicant}, 
                                  context_instance=RequestContext(request))
