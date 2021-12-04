
from django.db import models


class Article_info(models.Model):
    articleid = models.CharField(blank=True,max_length=100)
    title = models.CharField(blank=True,max_length=300)
    author = models.CharField(blank=True,max_length=100)
    publishdate = models.CharField(blank=True,max_length=100)
    srcurl = models.CharField(blank=True,max_length=500)
    articletype = models.CharField(blank=True,max_length=100)
    datadate = models.DateTimeField(auto_now_add=True)
    look = models.IntegerField(default = 0)
    instr = models.CharField(blank=True,max_length=5000)
    img = models.FileField(upload_to='articleimg',blank=True)
    authorurl = models.CharField(blank=True,max_length=500)
    articlecate = models.CharField(blank=True,max_length=100)
    src = models.CharField(blank=True,max_length=100)
    
class Article_img(models.Model):
    articleid = models.CharField(blank=True,max_length=100)
    imgname = models.CharField(blank=True,max_length=300)
    img = models.FileField(upload_to='articleimg')
    datadate = models.DateTimeField(auto_now_add=True)

class Article_content(models.Model):
    articleid = models.CharField(blank=True,max_length=100)
    pid = models.IntegerField(default = 0)
    ptype = models.CharField(max_length=100,blank=True)
    pstyle = models.CharField(max_length=100,blank=True)
    p = models.CharField(max_length=5000,blank=True)
    img = models.ForeignKey('Article_img',null=True)
    pimg = models.FileField(upload_to='articleimg',blank=True)












