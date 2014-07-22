# Create your views here.
import json

from django.core import serializers
from django.http import HttpResponse, HttpRequest
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from django.core import serializers
from django.conf import settings
from django import forms
from django.core.exceptions import ObjectDoesNotExist

from cloudchoice.models import Vendor, Product, Plan

def index(request):

    if settings.DEBUG:
        javascripts = ["underscore.js", "backbone.js"]
    else:
        javascripts = ["underscore-min.js", "backbone-min.js"]
    javascripts.append("cloudchoice/index.js")

    stylesheets = ["cloudchoice/style.css"]

    dataToTemplate = {
        'title'       : 'Choose A Cloud Vendor',
        'vendors'     : Vendor.objects.all(),
        'javascripts' : javascripts,
        'stylesheets' : stylesheets,
    }

    return render_to_response('cloudchoice/index.html', dataToTemplate, context_instance = RequestContext(request))

def list_vendors(request):
    body = "Here is the list"
    vendorSets = Vendor.objects.all()
    vendorS = dict()
    for vendor in vendorSets:
        vendorS[vendor.id] = vendor.name
    body = json.dumps(vendorS)
    return HttpResponse(body)

def list_products(request):
    productList = list()

    for plan in Plan.objects.all():
        node = dict()
        node['vendor'] = plan.product.vendor.name
        node['product_name'] = plan.product.product_name
        node['plan_name'] = plan.name
        node['offer'] = plan.product.offer
        node['unit'] = plan.unit.unit
        node['unit_amount'] = plan.unit_amount
        node['unit_price'] = '$%.2f' % plan.unit_price
        productList.append(node)
                
#    body = json.dumps(serializers.serialize("json", productList))
    body = json.dumps(productList)
    return HttpResponse(body)
