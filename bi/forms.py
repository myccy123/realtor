# -*- coding:utf-8 -*-
from django import forms


class Mysqlconn(forms.Form):
    mysqle_dataSource = forms.CharField(max_length=100)
    mysqle_permiss = forms.CharField(max_length=100)
    mysqle_ip = forms.CharField(max_length=100)
    mysqle_user = forms.CharField(max_length=100)
    mysqle_psw = forms.CharField(widget=forms.PasswordInput)
    mysqle_port = forms.CharField(max_length=10)

class Mysqltab(forms.Form):
    mysqle_dataSource = forms.CharField(max_length=100)
    mysqle_permiss = forms.CharField(max_length=100)
    mysqle_ip = forms.CharField(max_length=100)
    mysqle_user = forms.CharField(max_length=100)
    mysqle_psw = forms.CharField(widget=forms.PasswordInput)
    mysqle_port = forms.CharField(max_length=10)
    db = forms.CharField(max_length=50)
    tab = forms.CharField(max_length=50)
    checked = forms.CharField(max_length=10)

class Sourceid(forms.Form):
    sourceid = forms.CharField(max_length=100)
    
    