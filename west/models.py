from django.db import models

import sys
reload(sys)   
sys.setdefaultencoding('utf8')  







class weibo(models.Model):
    mid = models.BigIntegerField(primary_key=True)
    uname = models.CharField(max_length=40, blank=True)
    neirong = models.TextField(blank=True)
    yuanuname = models.CharField(max_length=40, blank=True)
    yuanneirong = models.TextField(blank=True)
    time = models.CharField(max_length=20, blank=True)
    here = models.CharField(max_length=20, blank=True)
    zan = models.IntegerField(blank=True, null=True)
    zhuanfa = models.IntegerField(blank=True, null=True)
    shoucang = models.IntegerField(blank=True, null=True)
    pinglun = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        #return '  %s :     %s' %(self.uname,self.neirong)
        return self.uname,self.neirong

    
    class Meta:
        ordering = ["mid"]

# Create your models here.
class sousuo(models.Model):
    sstime =models.DateTimeField(primary_key=True)
    ssneirong = models.CharField(max_length=100)
    def __str__(self):
        return self.ssneirong


