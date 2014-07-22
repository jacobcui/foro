from copy import copy
from django.db import models
from django.db.models.query import QuerySet
from school.models import School
import json, requests

class SchoolHelper(object):

    query = QuerySet(model=School)
    allsetcount = School.objects.count()
    allset = School.objects.all()
    url = 'http://maps.google.com/maps/api/geocode/json?sensor=false&components=country:AU&address='
    allvalid = []  ## all school which has location(lat, lng)
    
    def getAllSetCount(self):
        return self.allsetcount

    def getAllValid(self):
        for s in self.allset:
            if s.lat != None:
                self.allvalid.append(s);
        return self.allvalid
        
    def doesExists(self, name):
        self.name = name
        if self.query.filter(pk=name).exists():
            return True
        else:
            return False

    def getAllSet(self):    
        return self.allset

    def getLocation(self, address):
        url = self.url + address
        resp = requests.get(url);
        data = json.loads(resp.text)
        status = data['status']
        
        if status != "OK":
            return status

        res = data['results']
        self.lastaddresses = []
        loc = dict()
        for r in res:
#            print "\t%s (%s, %s)" % (r['formatted_address'], r['geometry']['location']['lat'], r['geometry']['location']['lng'])
            loc['lat'] =  r['geometry']['location']['lat']
            loc['lng'] =  r['geometry']['location']['lng']
            
            break
            #self.lastaddresses.append((r['geometry']['location']['lat'], r['geometry']['location']['lng']))
            #return copy(self.lastaddresses)    
        return copy(loc)

if __name__ == '__main__':
    sh = SchoolHelper()
    print sh.doesExists('Yeo park')
    print sh.doesExists('Yeo parka')
    schools  = sh.getAllValid()
    for s in schools:
        print s.name, " ", s.rank
