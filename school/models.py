from django.db import models

# Create your models here.
class School(models.Model):
#    id = models.AutoField(primary_key=True)
    name = models.CharField(primary_key=True, max_length = 128)
    rank = models.IntegerField()
    suburb = models.CharField(max_length = 64)
    score = models.IntegerField()
    link = models.CharField(max_length = 256)
    address = models.CharField(max_length = 256)
    lat = models.FloatField(null = True)
    lng = models.FloatField(null = True)
    def __unicode__(self):
        return "%s:%d" % (self.name, self.rank)

