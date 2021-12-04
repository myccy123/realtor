# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from singlepage.models import Listing_for_sp,Openhouse,Sp_img,Call_history,finance
from web.models import *

# Register your models here.


@admin.register(Listing_for_sp)
class Listing_for_spAdmin(admin.ModelAdmin):
    list_display = ('listingid', 'cityname','listingname','othermls',)
    search_fields = ('listingid','cityname','listingname','othermls',)
    list_filter = ('cityname',)
    readonly_fields = ('listingid',)
    fieldsets = (
        (None, {
            'fields': ('listingid','cityname', 'listingname','othermls','listingtype','url','distid',)
        }),
        ('listing info', {
            'fields': ('price','areas', 'bedroom','toilet','parking','tax','housetype','housestyle',
                       'basement','builddate','corp','vrtour','intro','intro_zh','lat','lng','titleagent',
                       'salestatus','isspread','mapspread')
        }),
    )

@admin.register(Openhouse)
class OpenhouseAdmin(admin.ModelAdmin):
    list_display = ('listingid', 'bgndate1','enddate1','bgndate2','enddate2',)
    search_fields = ('listingid',)
    list_filter = ('listingid',)
    fieldsets = (
        (None, {
            'fields': ('listingid', 'bgndate1','enddate1','bgndate2','enddate2',)
        }),
    )
    
@admin.register(agent_info)
class agent_infoAdmin(admin.ModelAdmin):
    list_display = ('userid', 'username','tel','username2','tel2',)
    search_fields = ('email','username',)
    list_filter = ('username',)
    readonly_fields = ('userid',)
    fieldsets = (
        ('国外经纪人信息', {
            'fields': ('userid','fname','lname','username','email', 'tel','note','corp','website','address','postid','selfintro','selfintro_cn'
                       ,'corpintro','corpintro_cn','teamintro','teamintro_cn','head','logo','qrcode','active','city',)
        }),
        ('国内经纪人信息', {
            'fields': ('username2', 'tel2','email2','head2','qrcode2',)
        }),
    )
    
@admin.register(Sp_img)
class Sp_imgAdmin(admin.ModelAdmin):
    list_display = ('listingid', 'imgtype','img','owner',)
    search_fields = ('listingid',)
    list_filter = ('listingid',)
    fieldsets = (
        (None, {
            'fields': ('listingid', 'imgtype','img','owner',)
        }),
    )

@admin.register(agent_card)
class agent_cardAdmin(admin.ModelAdmin):
    list_display = ('userid','holder', 'cardno','cardtype',)
    search_fields = ('userid','holder', 'cardno','cardtype',)
    list_filter = ('cardtype',)
    readonly_fields = ('userid','holder', 'cardno','expire','cvs', 'postid','cardtype',)
    fieldsets = (
        (None, {
            'fields': ('userid','holder', 'cardno','expire','cvs', 'postid','cardtype',)
        }),
    )
    
@admin.register(agent_auth)
class agent_authAdmin(admin.ModelAdmin):
    list_display = ('userid','service', 'fee','status','bgndate','enddate','cardno',)
    search_fields = ('userid','status', 'cardno',)
    list_filter = ('status',)
    fieldsets = (
        (None, {
            'fields': ('userid','service', 'fee','status','cardno','token','bgndate','enddate','invoice',)
        }),
    )

@admin.register(Call_history)
class Call_historyAdmin(admin.ModelAdmin):
    list_display = ('datadate','agentid', 'listingid','username','tel','email','description','ip',)
    search_fields = ('datadate',)
    list_filter = ('agentid',)
    readonly_fields = ('datadate','agentid', 'listingid','username','tel','email','description','ip',)
    fieldsets = (
        (None, {
            'fields': ('datadate','agentid', 'listingid','username','tel','email','description','ip',)
        }),
    )
