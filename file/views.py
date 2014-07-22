
# Create your views here.
import json
from django.template import RequestContext
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render_to_response
from django.core.context_processors import csrf

from mysite.utils import utils
from mysite.models import userfile

oUtils = utils();

## get file contents
def getfile(request, userid, filename):
    body = ""
    isGoodToGo = False
    errorMessage = ""

        
    if 'action' in request.GET:
        if 'appkey' in request.GET:
            appkey = request.GET['appkey']
            isGoodToGo = True
        else:
            errorMessage = "No appkey"
    else:
        isGoodToGo = True
        errorMessage = "Method is not supported."
    

        
    if isGoodToGo:
        files = oUtils.getUserFileByName(userid, filename)
        print len(files)

        if len(files) > 1: ## list
            for f in files:
                body = body + "<BR>" + f.filename
        else: #read a file
            fileNode = files[0]
            fileFullPath = oUtils.getFileDirectory(fileNode.filepath) + fileNode.filename
            f = open(oUtils.getFileDirectory(fileNode.filepath) + fileNode.filename, 'r' );
            body = ""
            body += body + f.read()

            response = HttpResponse(body, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = "attachment; filename=%s" % fileNode.filename

#            response = HttpResponse(mimetype='application/force-download')
#            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(fileNode.filename)
#            response['X-Sendfile'] = smart_str(fileFullPath)
        # It's usually a good idea to set the 'Content-Length' header too.
        # You can also set any other required headers: Cache-Control, etc.
            return response

    else:
        body = errorMessage

    
    return HttpResponse(body)


def getfilelist(request, userid):
    body = str(userid)
    return HttpResponse(body)
