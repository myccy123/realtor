from __future__ import unicode_literals

from django.db import models

class User_data(models.Model):
    chartid = models.CharField(max_length=50,unique=True)
    chartname = models.CharField(max_length=200,blank=True)
    charttype = models.CharField(max_length=50)
    userid = models.CharField(max_length=50)
    visualof = models.CharField(max_length=50)
    data = models.FileField(upload_to='chartdata')
    datatype = models.CharField(max_length=50,blank = True)
    dataicon = models.FileField(upload_to='charticon',blank = True)
    srctab = models.CharField(max_length=200,blank = True)
    srcid = models.CharField(max_length=200,blank = True)
    rttype = models.CharField(max_length=200,blank = True)
    timewindow = models.CharField(max_length=10,blank = True)
    theme = models.CharField(max_length=50,blank = True)

class Tmpdata(models.Model):
    data = models.FileField(upload_to='tmp')
    srctab = models.CharField(max_length=200,blank = True)
    sqls = models.CharField(max_length=5000,blank = True)
    rttype = models.CharField(max_length=200,blank = True)
    jsn = models.TextField(blank = True)
    timewindow = models.CharField(max_length=10,blank = True)

class Source(models.Model):
    sourceid = models.CharField(max_length=50)
    sourcename = models.CharField(max_length=50)
    sourcetype = models.CharField(max_length=50)
    sourcepermi = models.CharField(max_length=50)
    sourcefrom = models.CharField(max_length=50)
    datais = models.CharField(max_length=50,blank = True)
    isenable = models.CharField(max_length=1)
    sourceip = models.CharField(max_length=300,blank = True)
    sourceuser = models.CharField(max_length=300,blank = True)
    sourcepasswd = models.CharField(max_length=300,blank = True)
    sourceport = models.CharField(max_length=300,blank = True)
    sourcedb = models.CharField(max_length=300,blank = True)
    realtime = models.CharField(max_length=1,blank = True)

class Source_file(models.Model):
    sourceid = models.CharField(max_length=50,blank = True)
    filetype = models.CharField(max_length=50,blank = True)
    hashead = models.CharField(max_length=1,blank = True)
    file = models.FileField(upload_to='srcfile',blank = True)

class Template(models.Model):
    userid = models.CharField(max_length=50)
    tempid = models.CharField(max_length=50)
    status = models.CharField(max_length=10)
    tempname = models.CharField(max_length=50,blank = True)
    temptype = models.CharField(max_length=100,blank = True)
    savetime = models.DateTimeField(auto_now = True)
    htmldata = models.TextField(blank = True)
    htmlurl = models.CharField(max_length=100,blank = True)
    divdata = models.TextField(blank = True)
    divurl = models.CharField(max_length=100,blank = True)


class Echarts_Json_columns(models.Model):
    chartid = models.CharField(max_length=100)
    tablename = models.CharField(max_length=100)
    echart_columns = models.CharField(max_length=100)
    computation_rule = models.CharField(max_length=20,null=True,blank=True)
    chart_type = models.CharField(max_length=20,null=True,blank=True)
    xAxis_or_yAxis = models.CharField(max_length=20)
    yAxisIndex = models.CharField(max_length=20,null=True,blank=True)
    scaler = models.IntegerField()
    where_rule = models.CharField(max_length=200)
    savetime = models.DateTimeField(auto_now = True)


class Echarts_Json_info(models.Model):
    chartid = models.CharField(max_length=100)
    Json_file_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    subtext = models.CharField(max_length=100,null=True,blank=True)
    xunit = models.CharField(max_length=100,null=True,blank=True)
    lyunit = models.CharField(max_length=100,null=True,blank=True)
    ryunit = models.CharField(max_length=100,null=True,blank=True)
    lyname = models.CharField(max_length=100,null=True,blank=True)
    ryname = models.CharField(max_length=100,null=True,blank=True)
    formatter = models.CharField(max_length=100,null=True,blank=True)
    report_sql = models.CharField(max_length=500,null=True,blank=True)
    flag = models.CharField(max_length=100)
    savetime = models.DateTimeField(auto_now = True)