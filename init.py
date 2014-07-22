import os,sys,random,string
from copy import copy
from django.db import models
from django.db.models.query import QuerySet
from django.db.models import Max, Min
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from mysite.models import FbImage, userfile
from report.models import Plan as ExcelPlan, UserPlan as ExcelUserPlan
from report.utils import utils as ExcelUtils

reportUtils = ExcelUtils()
basecharge = 15 

## Excel Plan
excelPlan = None
try:
    excelPlan = ExcelPlan.objects.get(planid="developer")
except ObjectDoesNotExist:
    excelPlan = ExcelPlan( planid="developer" )

excelPlan.description = "Developer"
excelPlan.price = 0.0
excelPlan.length = -1
excelPlan.limit = reportUtils.record_limit
excelPlan.save()

try:
    excelPlan = ExcelPlan.objects.get(planid="commercial_1month")
except ObjectDoesNotExist:
    excelPlan = ExcelPlan( planid="commercial_1month" )

excelPlan.description = "Commercial Plan 1 Month"
excelPlan.price = basecharge
excelPlan.length = 1
excelPlan.limit = -1
excelPlan.save()

try:
    excelPlan = ExcelPlan.objects.get(planid="commercial_6month")
except ObjectDoesNotExist:
    excelPlan = ExcelPlan( planid="commercial_6month" )

excelPlan.description = "Commercial Semi Annual"
excelPlan.price = basecharge * 6 * 0.8
excelPlan.length = 6
excelPlan.limit = -1
excelPlan.save()

try:
    excelPlan = ExcelPlan.objects.get(planid="commercial_12month")
except ObjectDoesNotExist:
    excelPlan = ExcelPlan( planid="commercial_12month" )

excelPlan.description = "Commercial Annual"
excelPlan.price = basecharge * 12 * 0.8
excelPlan.length = 12
excelPlan.limit = -1
excelPlan.save()

try:
    excelPlan = ExcelPlan.objects.get(planid="commercial_partner")
except ObjectDoesNotExist:
    excelPlan = ExcelPlan( planid="commercial_partner" )

excelPlan.description = "Commercial Partner"
excelPlan.price = basecharge * 24 * 0.7 * 1.4
excelPlan.length = -1
excelPlan.limit = -1
excelPlan.save()


try:
    User.objects.get(username="demo");
except ObjectDoesNotExist:
    demoUser = User(username="demo", password="RT@$!l13351")
    demoUser.save()

demoUser = User.objects.get(username="demo");

try:
    demoExcelUserPlan = ExcelUserPlan.objects.get(user=demoUser)
except ObjectDoesNotExist:
    demoExcelUserPlan = ExcelUserPlan(user = demoUser)

demoExcelUserPlan.plan = ExcelPlan.objects.get(planid='developer')
demoExcelUserPlan.appkey = reportUtils.appkeys['APPKEY_DEMO']
demoExcelUserPlan.site = '*'
demoExcelUserPlan.save()
