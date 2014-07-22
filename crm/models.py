from django.db import models

# Create your models here.
import datetime
from django.utils import timezone

# Create your models here.
class Applicant(models.Model):
    index = models.IntegerField()
    op_date = models.DateTimeField('date published')
    first_name = models.CharField(max_length=200)
    last_name =  models.CharField(max_length=200)
    def __unicode__(self):
        return self.first_name + " " + self.last_name
    
class Contact(models.Model):
    contact = models.ForeignKey(Applicant)
    phone = models.CharField(max_length=200)
    mobile = models.CharField(max_length=200, blank=True, null=False)
    fax = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    def __unicode__(self):
        return self.contact.first_name + " " + self.contact.last_name
