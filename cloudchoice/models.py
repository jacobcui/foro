from django.db import models
from addressbook.models import Contact, Address, Email, PhoneNumber, SocialNetwork, Website

# Here is the map
#  Vendor A
#      \_____ Product A
#                \________Plan A
#                            \_______Component A
#                            \_______Component B
#                \________Plan B
#                            \_______Component C
#
#      \_____ Product B
#                \________Plan C
#                            \_______Component D
#                            \_______Component E
class ComponentName(models.Model):
    name = models.CharField(max_length = 255, unique = True)
    ## CPU, Mem, Storage, Network, 
    def __unicode__(self):
        return "%s" % self.name
        
class OS(models.Model):
    name = models.CharField(max_length = 255, unique = True)
    def __unicode__(self):
        return "%s" % self.name
    # Ubuntu....

class Unit(models.Model):
    unit = models.CharField(max_length = 32, unique = True)
    ## Month, Year, Hour, GB, Piece
    ## Virtual Core
    def __unicode__(self):
        return "%s" % self.unit

class CloudModel(models.Model):
    model = models.CharField(max_length = 16, unique = True)
    ## IaaS, PaaS, SaaS
    description = models.CharField(max_length=1024, null = True, blank = True)
    def __unicode__(self):
        return "%s" % self.model
        
class Service(models.Model):
    service = models.CharField(max_length = 64, unique = True)
    ## Web hosting, Sharpoint, Virtual Server, Email, etc
    description = models.CharField(max_length=1024, null = True, blank = True)
    def __unicode__(self):
        return "%s" % self.service

class Vendor(models.Model):
    name = models.CharField(max_length = 128, unique = True)
    contact = models.ForeignKey(Contact, blank=True, null=True)
    website = models.ForeignKey(Website, blank=True, null=True)
    address = models.ForeignKey(Address, blank=True, null=True)
    email =  models.ForeignKey(Email, blank=True, null=True)
    phonenumber = models.ForeignKey(PhoneNumber,blank=True, null=True)
    socialnetwork = models.ForeignKey(SocialNetwork,blank=True, null=True)
    def __unicode__(self):
        return "%s" % self.name
        
class Product(models.Model):
    vendor = models.ForeignKey(Vendor)
    cloudmodel = models.ForeignKey(CloudModel)
    service = models.ForeignKey(Service)
    product_name = models.CharField(max_length=128, unique = True)
    upfront = models.FloatField(default = 0.0)
    offer = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    def __unicode__(self):
        return "%s: %s" % (self.vendor, self.product_name)

class Plan(models.Model):
    product = models.ForeignKey(Product)
    name = models.CharField(max_length=128)
    unit = models.ForeignKey(Unit)
    unit_amount = models.FloatField(default = 1.0)
    unit_price = models.FloatField(default = 0.0)
    comment = models.TextField(blank=True, null=True)
    def __unicode__(self):
        return "%s: %s" % (self.product, self.name)

    
class Component(models.Model):
    plan = models.ForeignKey(Plan)
    name = models.ForeignKey(ComponentName)
    unit = models.ForeignKey(Unit)
    content = models.CharField(max_length=128, blank=True, null=True)
    amount = models.FloatField(default = 1)
    price = models.FloatField(default = 0.0)
    def __unicode__(self):
        return "%s: %s" % (self.plan, self.name)
