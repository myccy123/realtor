# -*- coding:utf-8 -*-
from django import forms


class Signup1(forms.Form):
    fname = forms.CharField(max_length=100)
    sname = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    userid = forms.CharField(max_length=100)
    passwd1 = forms.CharField(widget=forms.PasswordInput)
    passwd2 = forms.CharField(widget=forms.PasswordInput)



class Signup2(forms.Form):
    userid = forms.CharField(max_length=100)
    passwd1 = forms.CharField(widget=forms.PasswordInput)
    passwd2 = forms.CharField(widget=forms.PasswordInput)
    keynum = forms.CharField(max_length=6)
    cityname = forms.CharField(max_length=100)
    fname = forms.CharField(max_length=100)
    sname = forms.CharField(max_length=100)

class Signin(forms.Form):
    userid = forms.CharField(max_length=100)
    passwd = forms.CharField(widget=forms.PasswordInput)
    
class Setpasswd(forms.Form):
    userid = forms.CharField(max_length=100)
    passwd1 = forms.CharField(widget=forms.PasswordInput)
    passwd2 = forms.CharField(widget=forms.PasswordInput)
    passwd3 = forms.CharField(widget=forms.PasswordInput)
    
class Temp(forms.Form):
    tempid = forms.CharField(max_length=100)
    userid = forms.CharField(max_length=100)
    temptype = forms.CharField(max_length=100)
    temp = forms.CharField(max_length=100)

class Mkhtml(forms.Form):
    tempid = forms.CharField(max_length=100)
    userid = forms.CharField(max_length=100)
    dataid = forms.CharField(max_length=100,required=False)
    srtype = forms.CharField(max_length=100)
    tr = forms.CharField(max_length=1)
    sr = forms.CharField(max_length=1)

class Submitcomm(forms.Form):
    htmlid = forms.CharField(max_length=100)
    commtype = forms.CharField(max_length=20)
    userid = forms.CharField(max_length=100)
    usercomm = forms.CharField(max_length=500)

class Savelisting2(forms.Form):
    listingid = forms.CharField(max_length=100)
    listingname = forms.CharField(max_length=100)
    cityname = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    proaddress = forms.CharField(max_length=100)
    price1 = forms.CharField(max_length=100)
    price2 = forms.CharField(max_length=100)
    areas = forms.CharField(max_length=100)
    postid = forms.CharField(max_length=100)
    housetype = forms.CharField(max_length=100)
    intro = forms.CharField(widget=forms.Textarea)
    corp = forms.CharField(max_length=100)
    warning = forms.CharField(max_length=100)
    opendate = forms.CharField(max_length=100)

class Saveimg(forms.Form):
    id = forms.CharField(max_length=100)
    imgtype = forms.CharField(max_length=100)
    img = forms.FileField()

class Payinfo(forms.Form):
    token = forms.CharField(max_length=100)
    amt = forms.CharField(max_length=100)
    curr = forms.CharField(max_length=3)
    userid = forms.CharField(max_length=100)

class Orderinfo(forms.Form):
    htmlid = forms.CharField(max_length=100)
    userid = forms.CharField(max_length=100)
    dataid = forms.CharField(max_length=100)
    ordertype = forms.CharField(max_length=10)
    transid = forms.CharField(max_length=100)

