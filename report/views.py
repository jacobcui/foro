# Create your views here.
import json, os

from django.template import RequestContext
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from mysite.utils import utils
from report.genfile import genfile
from report.models import Plan as ExcelPlan
import report.utils

oUtils = utils()
reportUtils = report.utils.utils()
def gencsrf(request):
    return render_to_response('report/gencsrf.html', {}, context_instance = RequestContext(request))

def getPlan(request, planid):
    plan = None
    try:
        plan = ExcelPlan.objects.get(planid=planid)
    except ObjectDoesNotExist:
        return render_to_response('404.html', {}, context_instance = RequestContext(request))
        
    dataToTemplate = {
        'sitename': settings.SITENAME,
        'planid': planid,
        'price' : plan.price,
        'length' : plan.length,
        'planname' : plan.description,
        'cost' : plan.price,
        'sales_email' : settings.SALES_EMAIL
    }
  
    return render_to_response('report/getplan.html', dataToTemplate, context_instance = RequestContext(request))

def index(request):
    stylesheets = ["construction.css"]
    dataToTemplate = {"stylesheets": stylesheets,         
                      'sitename': settings.SITENAME}
    return render_to_response('baseconstruction.html', dataToTemplate, context_instance = RequestContext(request))

def generate_form(request):
    return render_to_response('baseconstruction.html', dataToTemplate, context_instance = RequestContext(request))

def generate(request):
    body = ""
    retdata = {
        'statuscode': -1,
        'errormessage': '',
        'filelink' : '',
        'filename' : ''
    }

    isGoodToGo = False
    format = ""
    data = ""
    appkey = ""

    if 'seq' in request.GET and 'token' in request.GET and 'total' in request.GET and 'action' in request.GET and 'appkey' in request.GET and 'data' in request.GET and 'format' in request.GET:
        format = request.GET['format']
        if format == 'json' or format == 'text':
            isGoodToGo = True
                    
            data = request.GET['data']
            appkey = request.GET['appkey']
    else:                
        retdata['statuscode'] = reportUtils.ret_code['INVALID_PARAMS']
        retdata['errormessage'] = reportUtils.ret_message['INVALID_PARAMS']
        body = json.dumps(retdata, sort_keys=True, indent=4);            
        return HttpResponse("parseResponse(" + body + ");")

    ## Not in GET

    xlsdata = request.GET['data']
    javascripts = ["report/download.js"]
    stylesheets = ["report/download.css"]

    # seq starts from 1
    seq = int(request.GET['seq'])
    total = int(request.GET['total'])
    user = reportUtils.getUserByAppKey(appkey);
    if user is None:
        retdata['errormessage'] = reportUtils.ret_message['APPKEY_NOT_FOUND']
        retdata['statuscode'] = reportUtils.ret_code['APPKEY_NOT_FOUND']
        body = json.dumps(retdata, sort_keys=True, indent=4);            
        return HttpResponse("parseResponse(" + body + ");")

    
    #user.username:
    #    retdata['errormessage'] = retdata['errormessage'] + " " + "Invalid appkey."
    #    retdata['statuscode'] = reportUtils.ret_code['NOT_FOUND']
    #    body = json.dumps(retdata, sort_keys=True, indent=4);            
    #    return HttpResponse(body)
    userid = user.id
    fileDirectory = oUtils.getFileDirectory(userid);
    cacheFileDirectory = fileDirectory + request.GET['token']
    cacheFilePath = "%s/%d" % (cacheFileDirectory, seq)

    if not os.path.exists(cacheFileDirectory):
        try:
            os.makedirs(cacheFileDirectory)
        except os.error:
            retdata['errormessage'] = os.error.strerror
            retdata['statuscode'] = 10
            return HttpResponse(body)

    cacheFile = None
    try:
        cacheFile = open(cacheFilePath, 'w')
    except os.error:
        retdata['statuscode']   = reportUtils.ret_code['NOT_FOUND']
        retdata['errormessage'] = reportUtils.ret_message['NOT_FOUND']
        retdata['processed']    = str(seq)
        retdata['total']        = str(total)
        body = json.dumps(retdata, sort_keys=True, indent=4);            
        return HttpResponse("parseResponse(" + body + ");")

    if seq <= total:
        cacheFile.write(xlsdata)
        cacheFile.close()

    if seq < total:
        retdata['statuscode']   = reportUtils.ret_code['PARTIAL_OK']
        retdata['errormessage'] = reportUtils.ret_message['PARTIAL_OK']
        retdata['processed']    = str(seq)
        retdata['total']        = str(total)
        body = json.dumps(retdata, sort_keys=True, indent=4);            
        return HttpResponse("parseResponse(" + body + ");")

    ## collect files
    xlsdata = reportUtils.collectFiles(cacheFileDirectory, total)

    ret = 0
    fileName = ""
    limit = reportUtils.record_limit;
    ## check app key
    REMOTE_HOST = ""
    if 'REMOTE_HOST' in request.META:
        REMOTE_HOST = request.META['REMOTE_HOST']

    if 0 == reportUtils.validateAppKey(appkey, (request.META['REMOTE_ADDR'], REMOTE_HOST)) :
        limit = reportUtils.getLimit(appkey)
    else:
        retdata['statuscode'] = reportUtils.ret_code['UNKNOWN_SITE']
        retdata['errormessage'] = reportUtils.ret_message['UNKNOWN_SITE']
        body = json.dumps(retdata, sort_keys=True, indent=4);            
        return HttpResponse("parseResponse(" + body +");")
    
    fileName  = oUtils.getRandomString(8) + ".xls"
    fileRelDir = str(userid)

    if not os.path.exists(fileDirectory):
        try:
            os.makedirs(fileDirectory)
        except os.error:
            print os.error.strerror
            retdata['errormessage'] = os.error.strerror
            retdata['statuscode'] = 10
            return HttpResponse(body)
            
    fullFilePath = fileDirectory  + fileName
        
    gf = genfile()
    gf.setLimit(limit)

    if format == 'json':
        try:
            feedData = json.loads(xlsdata)
        except:
            retdata['statuscode'] = reportUtils.ret_code['INVALID_FORMAT']
            retdata['errormessage'] = reportUtils.ret_message['INVALID_FORMAT']
            body = json.dumps(retdata, sort_keys=True, indent=4);            
            return HttpResponse("parseResponse(" + body + ");")

        ret = gf.genXlsByJson(feedData, fullFilePath)
    elif format == 'text':
        ret = gf.genXlsByText(xlsdata, fullFilePath)
    
    if 0 != ret :
        retdata['statuscode'] = reportUtils.ret_code['INVALID_FORMAT']
        retdata['errormessage'] = reportUtils.ret_message['INVALID_FORMAT']
        body = json.dumps(retdata, sort_keys=True, indent=4);            
        return HttpResponse("parseResponse(" + body + ");")


    filelink = "/file/%d/%s" % (userid, fileName);
    retdata['statuscode'] = ret
    retdata['link'] = filelink
    retdata['filename'] = fileName
    oUtils.saveUserFileByName(userid, fileName, fileRelDir)
        
    body = json.dumps(retdata, sort_keys=True, indent=4);            
#        return render_to_response('report/download.html', dataToTemplate, context_instance = RequestContext(request)
    return HttpResponse("parseResponse(" + body + ");")


def test(request):
    if request.POST:
        return HttpResponseRedirect('/report/generate')

    javascripts = ["report/test.js", "report/jquery-text2excel.js"]
    stylesheets = ["report/test.css"]

    data = list()
    data.append(['Company Name',      'Last Sale', '+ or - ', 'Quote Buy', 'Quote Sell'])
    data.append(['Adelaide Brighton', 3.34,  -6.0,   3.33,  3.34])
    data.append(['AGL Energy',        15.56,  21.0, 15.51, 15.56])
    data.append(['ALS',               10.31, -22.0, 10.27, 10.33])
    data.append(['Amcor',             9.67,   19.0,  9.61,  9.67])
    data.append(['AMP',               5.15,   9.0,   5.15,  5.16])
    data.append(['Ansell',            15.12, -29.0, 15.12, 15.16])
    data.append(['ANZ Banking Grp',   28.69,  44.0, 28.67, 28.70])
    data.append(['APA Grp stp',       6.12,  -4.0,   6.12,  6.14])
    data.append(['Aristocrat Leisure',3.71,   2.0,   3.71,  3.73])
    data.append(['ASX',              36.62,  18.0,  36.61, 36.65])
    data.append(['Aurizon Hldgs',     3.94,  -4.0,   3.94,  3.95])
    data.append(['Aust Foundation',   5.38,  -7.0,   5.38,  5.41])
    data.append(['Aust Infrastructure Fd unt', 3.11, 3.0,   3.10, 3.11])
    data.append(['Australand Prop stp', 3.58,  4.0,  3.57,  3.58])

    textdata = ""

    datab = list()
    datab.append(['Company Name', 'Last Sale', "+ or -", 'Quote Buy', 'Quote Sell'])
    datab.append(['Bank of Qld',  9.57,       -1.0,      9.55,        9.57])
    datab.append(['Bendigo & Adelaide Bk',  10.29,  3.0,   10.25,   10.29])
    datab.append(['BlueScope Steel',         4.90,  1.0,    4.89,    4.90])
    datab.append(['Boral',                   4.97,  3.0,    4.96,    4.97])
    datab.append(['Brambles',                8.40,  7.0,    8.40,    8.41])
    datab.append(['Brickworks',             13.00, -6.0,   13.00,   13.05])

    xlsdata = {
        "Group A": data,
        "Group B": datab
        }

    xlsdataString = json.dumps(xlsdata, sort_keys=True, indent=4)

    for s in xlsdata:
        textdata += "[%s]\n" % s
        for row in xlsdata[s]:
            tmprow = list()
            for cell in row:
                cell = str(cell)
                tmprow.append(cell)
            textdata = textdata + ",".join(tmprow)
            textdata = textdata + "\n"
    

    dataToTemplate = {
        'sitename': settings.SITENAME,
        'javascripts' : javascripts,
        'stylesheets': stylesheets,
        'xlsdata': xlsdataString,
        'textdata': textdata,
        'userid': 5555,
        }
    return render_to_response('report/test.html', dataToTemplate, context_instance = RequestContext(request))


if __name__ == "__main__":
    reportPlan = Plan()
    # unit, kbytes
    discount = 0.8
    baseprice = 30
    baselength = 1

    
