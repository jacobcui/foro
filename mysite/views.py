# Create your views here.
import json
import sys
from django.core import serializers
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
import xml.etree.ElementTree as ET
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.files import File
from django import forms
from django.core.exceptions import ObjectDoesNotExist

from mysite.utils import utils
from report.utils import utils as reportutils
from report.models import Plan as ExcelPlan, UserPlan as ExcelUserPlan
from mysite.models import ContactUs
from panoview.models import SceneDetail, Scenes

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
#    cc_myself = forms.BooleanField(required=False)

def contact(request):
    form = ContactForm() 
    dataToTemplate = {
        'title': 'Get in touch',
        'form': form,
        'support_email': settings.SUPPORT_EMAIL,
    }
    errmsg = ""
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            anycontact = ContactUs(subject=form['subject'],
                                   message=form['message'],
                                   sender=form['sender']
            )
            anycontact.save()
            return render_to_response('contact_ok.html', dataToTemplate, context_instance = RequestContext(request))
        else:
            errmsg = "Please check input."
            dataToTemplate['errmsg'] = errmsg
    return render_to_response('contact.html', dataToTemplate, context_instance = RequestContext(request))

def cert(request):
    return render_to_response('NQ4bch2.html', {}, context_instance = RequestContext(request))

def signup(request):
    dataToTemplate = {'title': 'Sign up!'}    
    res = 0
    user = 0
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    # Redirect to a success page.
                    res = 1
    if res:
        login(request, user)
        return profile(request)
    else:
        form = UserCreationForm()
        dataToTemplate = {'title': 'Sign up!', 'form': form}    
        return render_to_response('signup.html', dataToTemplate, context_instance = RequestContext(request))

    
def terms(request):
    dataToTemplate = {
        'title': 'Foro terms and conditions',
        'sitename': settings.SITENAME
}
    return render_to_response('terms.html', dataToTemplate, context_instance = RequestContext(request))

def privacy(request):
    dataToTemplate = {
        'title': 'Privacy statement',
        'sitename': settings.SITENAME,
        'sales_email': settings.SALES_EMAIL
    }
    return render_to_response('privacy.html', dataToTemplate, context_instance = RequestContext(request))

def about(request):
    dataToTemplate = {
        'title': 'About us',
        'sitename': settings.SITENAME
    }
    return render_to_response('about.html', dataToTemplate, context_instance = RequestContext(request))
    
def getApplication(request, appname):
    javascripts = ["report/get_excel.js"]
    stylesheets = []

    dataToTemplate = {
        'home_active' : 'active',
        'javascripts' : javascripts,
        'stylesheets': stylesheets,
        }
    
    if appname == 'excel':
        reportUtils = reportutils()
        dataToTemplate['plans'] = ExcelPlan.objects.all()
        for p in ExcelPlan.objects.all():
            if p.length == -1:
                p.length = '120';
        return render_to_response('get-excel2.html', dataToTemplate, context_instance = RequestContext(request))
    
    return render_to_response('get-excel.html', dataToTemplate, context_instance = RequestContext(request))        

def profile(request):
    if request.user.is_authenticated():
        excelUserPlan = None
        try:
            excelUserPlan = ExcelUserPlan.objects.get(user=request.user)
        except ObjectDoesNotExist:
            excelUserPlan = ExcelUserPlan(user=request.user, plan=ExcelPlan.objects.get(planid='developer'), site='*')
            excelUserPlan.appkey = "DEVLOP_PLAN"
            excelUserPlan.save()

        if  excelUserPlan.appkey is None:
            excelUserPlan.appkey = "DEVLOP_PLAN"
            excelUserPlan.save()

        print excelUserPlan
        dataToTemplate = {
            'title': 'User Profile',
            'sitename': settings.SITENAME,
            'appname_excel': settings.APPNAME_EXCEL,
            'profile_active': 'active',
            'userplan_excel': excelUserPlan,
        }
        return render_to_response('profile.html', dataToTemplate, context_instance = RequestContext(request))
    else:
        return index(request)

def getstartted(request):
    dataToTemplate = {
        'getstartted_active': 'active',
        'sitename': settings.SITENAME,
        'javascripts': ["mysite/login.js"],
        'appname_excel': settings.APPNAME_EXCEL,
        'support_email': settings.SUPPORT_EMAIL,
    }
    return render_to_response('get-startted.html', dataToTemplate, context_instance = RequestContext(request))

def getresource(request, resource, username, textid, index, options):
    oUtils = utils()

    dataToTemplate = {        
        'pv_username' : username,
        'pv_textid' : textid,
        'pv_index' : index,
        'pv_options': options
    };

    try:
        scene_xml = oUtils.getPanoviewSceneXML(username, textid)
        tree = ET.parse(scene_xml)    
        root = tree.getroot()

        position_dict = {'u': 'Up',
                         'd': 'Down',
                         'l': 'Left',
                         'r': 'Right',
                         'b': 'Back',
                         'f': 'Front',
                         'fp': 'FloorPlan',
                         'c': 'Camera',
                         'ra': 'Radar',
        }

        image_dict = dict()
        image_dict['FloorPlan'] = root.find('./FloorMap/Image').text
        image_dict['Camera'] = root.find('./Camera/Image').text

        image_dict['Radar'] = root.find('./Radar/Image').text

        radar_number = root.find('./Coords/Amount').text

    except:
        print "can't find scene_xml for user:%s, textid: %s" % (username, textid)
        return HttpResponse("")

    scene = 0
    for s in root.findall('./Scene'):
        if s.find('Index').text == index:
            scene = s
            break

    if resource == 'scene':
        for texture in scene.findall('./SceneDetail/Textures/Texture'):
            image_dict[texture.find('Position').text] = texture.find('Image').text

        try:
            image_file = oUtils.getPanoviewFileDirectory(username, textid, image_dict[position_dict[options]]);
            image = File(open(image_file))
            image.open()
            print image_file
        except:
            print "Could not find image %s" % (image_file)
            return HttpResponse("")

        return HttpResponse(image.read(),  content_type = "image/png")

    if resource == 'pano':
        print "hit pano"
        return show_pano(request, resource, username, textid, index, options)

    try:
        radar_poss = [];
        for coord in root.findall('./Coords/Coord'):
            radar_poss.append(dict(x=coord.find('Lat').text, y=coord.find('Lon').text, i=coord.find('Index')))

        #radar_poss = [dict(x=0, y=0), dict(x=0, y=100), dict(x=100, y=100), dict(x=100, y=0)]
        dataToTemplate['pv_radar_number'] = radar_number
        if oUtils.isInOption(options, 'fs'): # full screen
            dataToTemplate['pv_scene_width'] = "window.innerWidth"
            dataToTemplate['pv_scene_height'] = "window.innerHeight"
        else:
            dataToTemplate['pv_scene_width'] = scene.find('./SceneDetail/Width').text
            dataToTemplate['pv_scene_height'] = scene.find('./SceneDetail/Height').text

        dataToTemplate['pv_scene_name'] = scene.find('./Name').text
        dataToTemplate['pv_radar_count'] = len(radar_poss)
        dataToTemplate['pv_radar_poss'] = radar_poss
        
        return render_to_response(resource, dataToTemplate, context_instance = RequestContext(request), content_type="text/javascript")
    except ObjectDoesNotExist:
        print "Object doesn't exist"
        return HttpResponseNotFound()
    except:
        print "sth happened"
        return HttpResponseNotFound()

def index(request):
    js_resource = ["/get/pv.js/panoview/main/2/0"]
    javascripts = ["three.min.js", "CSS3DRenderer.js", "underscore.js", "backbone.js", "pv.app.js"]
    stylesheets = ["pv.css"]
    
    dataToTemplate = {
        'home_active' : 'active',
        'javascripts' : javascripts,
        'js_resource' : js_resource,
        
        'sitename': settings.SITENAME,
        'appname_excel': settings.APPNAME_EXCEL,
        'stylesheets': stylesheets,
        }
#    return render_to_response('fake-index.html', dataToTemplate, context_instance = RequestContext(request))
    return render_to_response('index.html', dataToTemplate, context_instance = RequestContext(request))

def show_pano(request, resource, username, textid, index, options):
    js_resource = ["/get/pv.js/%s/%s/%s/%s" %(username, textid, index, options)]
    javascripts = ["three.min.js", "CSS3DRenderer.js", "underscore.js", "backbone.js", "pv.app.js"]
    stylesheets = ["pv.css"]
    ## print options
    dataToTemplate = {
#        'home_active' : 'active',
        'javascripts' : javascripts,
        'js_resource' : js_resource,
        
        'sitename': settings.SITENAME,
        'stylesheets': stylesheets,
        'username' : username,
        'textid' : textid,
        }

    return render_to_response('show_pano_fullscreen.html', dataToTemplate, context_instance = RequestContext(request))


def listpictures(request):
    oUtils = utils()
    randCount = 0
    if('count' in request.GET):
        randCount = request.GET['count']

    if randCount < 1:
        randCount = 10

    imgSet = oUtils.getRandomSet(randCount)
    imgDict = dict()
    for img in imgSet:
        imgDict[img.id] = img.facebookid
    body = json.dumps(imgDict)

    for img in imgSet:
        body = body + str(img.facebookid)
    return HttpResponse(body)

def http_404(request):
    return render_to_response('404.html')

def http_500(request):
    return render_to_response('500.html')

def http_505(request):
    return render_to_response('505.html')

if __name__ == "__main__":
    print oUtils.getImageDirectory();


    
