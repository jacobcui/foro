from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SceneDetail(models.Model):
    id = models.AutoField(primary_key=True)
    textid = models.CharField(max_length=64, unique=True) 
    width = models.CharField(max_length=256) # width can be anything
    height = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    def __unicode__(self):
        return "textid:%s, name:%s, width: %s , height: %s" % (self.textid, self.name, self.width, self.height);
        
class Scenes(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    detail = models.ForeignKey(SceneDetail)
    def __unicode__(self):
        return "%s : %s" % (self.user, self.detail)
