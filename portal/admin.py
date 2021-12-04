# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *
from web.models import *


# Register your models here.


@admin.register(FriendCorp)
class FriendCorpAdmin(admin.ModelAdmin):
    list_display = ('name', 'corp_url', 'logo', 'qr_code')
    readonly_fields = ()
    list_filter = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'corp_url', 'logo', 'qr_code')
        }),
    )


@admin.register(agent_img)
class agent_imgAdmin(admin.ModelAdmin):
    list_display = ('userid', 'imgtype', 'img',)
    search_fields = ('userid', 'imgtype',)
    list_filter = ('userid', 'imgtype',)
    fieldsets = (
        (None, {
            'fields': ('userid', 'imgtype', 'img',)
        }),
    )


@admin.register(MessageCenter)
class MessageCenterAdmin(admin.ModelAdmin):
    list_display = (
        'msg_type', 'mls', 'agentid', 'user_name', 'user_tel', 'user_email',
        'user_msg', 'user_ip', 'src_url', 'datadate')
    readonly_fields = ()
    list_filter = ('msg_type', 'mls', 'agentid', 'user_name',)
    fieldsets = (
        (None, {
            'fields': (
                'msg_type', 'mls', 'agentid', 'user_name', 'user_tel',
                'user_email',
                'user_msg', 'user_ip', 'src_url', 'datadate')
        }),
    )
