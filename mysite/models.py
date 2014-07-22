from django.db import models

# Create your models here.
class ContactUs(models.Model):
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=1024)
    sender = models.EmailField()
#    cc_myself = models.BooleanField(null=False)
    def __unicode__(self):
        return "%s:%s" % (self.sender, self.subject)
                          
class FbImage(models.Model):
    id = models.AutoField(primary_key=True)
    facebookid = models.BigIntegerField()
    name = models.CharField(max_length = 64)
    size = models.IntegerField()
    def __unicode__(self):
        return "%s:%d" % (self.name, self.size)

class userfile(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.IntegerField(primary_key=False)
    filename = models.CharField(max_length = 64 )
    filepath = models.CharField(max_length = 128)
    filesize = models.IntegerField(null=True)
    validtime = models.IntegerField(null=True)  ## hours
