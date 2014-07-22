import os,sys,random,string,shutil
from copy import copy
from django.db import models
from django.db.models.query import QuerySet
from django.db.models import Max, Min
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from mysite.models import FbImage, userfile
from report.models import Plan, UserPlan
from time import sleep

class utils(object):
    ret_code = {
        'INVALID_FORMAT' : 0x50,
        'INVALID_PARAMS': 0x40,
        'UNKNOWN_SITE': 0x30,
        'APPKEY_NOT_FOUND': 0x20,
        'NOT_FOUND': 0x10,
        'PARTIAL_OK': 0,
        'OK': 0
    }

    record_limit = 50
    timeout = 600 # 10 minutes

    ret_message = {
        'INVALID_FORMAT' : "Invalid data format.",
        'INVALID_PARAMS': "Invalid caller parameters",
        'UNKNOWN_SITE': "Unknown site",
        'APPKEY_NOT_FOUND': "Appkey doesn't exist",
        'NOT_FOUND': 'Object not found',
        'PARTIAL_OK':   'Partial Success',
        'OK':   'Success',
    }
    
    appkeys = {
        'APPKEY_DEMO': 'APPDEMO_EXCEL',
        'APPKEY_DEVELOPER': 'EXCELDEVELOPER',
    }
    
    price = {
        'plan':{
            'personal': 12,
            'budget': 24,
            'ultimate': 36,
        },
        'length':{
            'month': 1,
            'year1': 12,
            'year2': 24,
        },
        'length_name':{
            'month': 'monthly plan',
            'year1': '1 year plan',
            'year2': '2 year plan',
        },
        'discount': {
            'personal': 1,
            'budget': 0.8,
            'ultimate': 0.8,
            'month': 1,
            'year1': 0.8,
            'year2': 0.6,
        },
    }
    plan = {}

    def getUserByAppKey(self, appkey):
        try:
            userplan = UserPlan.objects.get(appkey=appkey);
            return userplan.user
        except ObjectDoesNotExist:
            return None
            
    # caller is tuple type
    def validateAppKey(self, appkey, caller):
        userplan = None
        try:
            userplan = UserPlan.objects.get(appkey=appkey)
        except ObjectDoesNotExist:
            return self.ret_code['APPKEY_NOTFOUND']

        sites = userplan.site
        if sites is None:
            return self.ret_code['UNKNOWN_SITE'] # not found

        sites = sites.split(',')
        for c in caller:
            for s in sites:
                if c == s or s == '*':
                    return self.ret_code['OK']

        return self.ret_code['NOT_FOUND'] # not found

    def collectFiles(self, directory, total):
        
        seq = 1
        total = int(total)
        timeout = 0
        text = ""

        while(seq <= total and timeout < self.timeout):
            try:
                file = "%s/%d" % (directory, seq)
                f = open(file, 'r')
                text = text + f.read()
                f.close()
                seq = seq + 1
            except os.error:
                print os.error.stderror
                sleep(1)
                timeout = timeout + 1

#        try:
#            shutil.rmtree(directory)
#        except os.error:
#            print os.error.stderror
        return text
        
    def  getPlan(self):
        for l in self.price['length']:
            for p in self.price['plan']:
                self.plan[p + '_' + l] = self.price['plan'][p] * self.price['discount'][p] * self.price['discount'][l]
                self.plan[p + '_' + l + '_length'] = self.price['length'][l]
                self.plan[p + '_' + l + '_name'] = p.capitalize() + " " + self.price['length_name'][l]
        return copy(self.plan)

    def getLimit(self, appkey):
        userplan = None
        try:
            userplan = UserPlan.objects.get(appkey=appkey)
        except ObjectDoesNotExist:
            return self.ret_code['APPKEY_NOTFOUND']

        if userplan.plan is None:
            return self.record_limit

        return userplan.plan.limit

    def attachPlan(self, userid, planid, option, site):
        userplan = User.objects.get(id=userid);
        return 0

    def getUserPlan(self, username):
        userplan = User.objects.get(username=username);
        return userplan

if __name__ == "__main__":
    o = utils()
    ps = o.getPlan()
    for a in ps:
        print 'Plan name: ' , a , "\t price: " , ps[a]
