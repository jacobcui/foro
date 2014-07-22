from time import sleep
from copy import copy
from string import find
from HTMLParser import HTMLParser, HTMLParseError

import django

from django.db import models
from school.models import School
import json, requests

from school.helper import SchoolHelper

helper = SchoolHelper()
allset = helper.getAllSet()

allsetcount = helper.getAllSetCount()

locations = []
i = 1;
for s in allset:
#    if s.lat is None:
    if i >= 552:
        address = s.name + "," + s.address;
        latlng = helper.getLocation(address) 
        if( type(latlng) is not dict):
            print "Request error: ", latlng, " for address ", address
            break
        s.lat = latlng['lat']
        s.lng = latlng['lng']
        s.save()
        sleep(1)
        print "%20s: %f, %f (%d/%d)" % (s.name, s.lat, s.lng, i, allsetcount)    
    i = i + 1
#    if i > 2:
#        break
    

