
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Plan(models.Model):
    id = models.AutoField(primary_key=True)
    planid = models.CharField(max_length = 64, unique=True)
    description = models.CharField(max_length=256)
    price = models.FloatField()
    length = models.IntegerField()
    limit = models.IntegerField()
    def __unicode__(self):
        return "%s : %s : %.2f : %i months : %i records" % (self.planid, self.description, self.price, self.length, self.limit)

class UserPlan(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    plan = models.ForeignKey(Plan)
    option = models.CharField(max_length = 32, null=True)
    expire = models.DateField(null=True)
    appkey =  models.CharField(max_length = 32, null=True)
    site =  models.CharField(max_length = 128, null=True)
    def __unicode__(self):
        return "%s : %s : %s : %s " % (self.user.username, self.plan.description, self.appkey, self.site)
