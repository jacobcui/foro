import commands, time, sys
import json, requests
from mysite.utils import utils
from mysite.models import FbImage

oUtils = utils()
iMaxFbId = oUtils.getMinFbId();
if not iMaxFbId:
    iMaxFbId = 100001437118470;

sPath = oUtils.getImageDirectory('fb')

url = "http://graph.facebook.com/"
id = iMaxFbId - 1
url_suffix = "/picture"
picture_format = ".jpg"

iLimit = 40000
while iLimit > 0:
    filename = "%d%s" % (id, picture_format)
    try:
        with open(filename):
            print "file %s exists. \r" % filename
    except IOError:
        idurl = "%s%d" % (url, id);
        resp = requests.get(url=idurl)
        json_obj = json.loads(resp.text)

        if 'error' in json_obj:
            print "this %d doesn't exists" % id
        else:
            cmd = "lwp-download %s%d%s %s%s" % (url, id, url_suffix, sPath, filename)
            print cmd + "\r"
            (res, buffer) = commands.getstatusoutput(cmd)
    except KeyboardInterrupt:
        print "Bye"
        sys.exit()
    
    iLimit = iLimit - 1
    id = id - 1
