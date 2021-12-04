# -*- coding:utf-8 -*-
from django.contrib import admin
from models import Article,Listing,Systemorder,Custom,Feedback,Userimage,Advertisement,Listingimg
from app.models import System_msg,Publish_apk

# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    
#     def formfield_for_dbfield(self, db_field, **kwargs):  
#         if db_field.name=='pro':  
#             kwargs['widget']=forms.Textarea  
#             try:  
#                 del kwargs['request']  
#             except KeyError:  
#                 pass  
#             return db_field.formfield(**kwargs)  
#         return super(ArticleAdmin, self).formfield_for_dbfield(db_field, **kwargs) 
    ordering = ['-article_id']
    list_display = ('title', 'pro')
    readonly_fields = ('article_id','article_type', 'title', 'pro',)
    list_filter = ('article_type',)
    fieldsets = (
        (None, {
            'fields': ('article_id','article_type', 'title', 'pro', 'eng_title')
        }),
    )
    
@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('listingid', 'cityname','listingname')
    readonly_fields = ('listingid','cityname', 'listingname',
                       'price','areas', 'bedroom','toilet','parking','tax','housetype','housestyle','basement','builddate','corp','intro',)
    search_fields = ('listingid','cityname','listingname',)
    list_filter = ('cityname',)
    fieldsets = (
        (None, {
            'fields': ('listingid','cityname', 'listingname',)
        }),
        ('listing info', {
            'fields': ('price','areas', 'bedroom','toilet','parking','tax','housetype','housestyle','basement','builddate','corp','intro','intro_eng',)
        }),
    )

@admin.register(Systemorder)
class SystemorderAdmin(admin.ModelAdmin):
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "status":
            kwargs['choices'] = (
                ('pending','待处理'),
                ('completed','推广中'),
            )
            if request.user.is_superuser:
                kwargs['choices'] += (('shared','已结束'),('commented','已评价'),)
        return super(SystemorderAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)
    list_display = ('starttime','htmlid', 'userid','ordertype','status',)
    list_editable = ('status',)
    readonly_fields = ('transid','starttime','htmlid', 'userid','dataid','ordertype',)
    search_fields = ('htmlid','userid','ordertype',)
    list_filter = ('status',)
    fieldsets = (
        (None, {
            'fields': ('starttime','htmlid','userid','dataid','transid','ordertype','status',)
        }),
    )
    

@admin.register(Custom)
class CustomAdmin(admin.ModelAdmin):
    list_display = ('userid','username','cityname','bedroom','toilet','usercity','tel','pricezone','buydate','addservice','datadate','housetype','notes')
    readonly_fields = ('cityname','bedroom','toilet','userid','username','usercity','tel','pricezone','buydate','addservice','datadate','housetype','notes')
    search_fields = ('cityname','username','userid','usercity',)
    list_filter = ('cityname',)
    def customs(self,obj):
        return 'customs'
    customs.short_description = '私人订制'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('userid','problem','idea','tel','email','datadate')
    readonly_fields = ('userid','problem','idea','tel','email','datadate','img1','img2','img3')
    search_fields = ('userid','tel','email',)

@admin.register(System_msg)
class System_msgAdmin(admin.ModelAdmin):
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "msgstatus":
            kwargs['choices'] = (
                ('pending','待发送'),
                ('sended','已发送'),
            )
        return super(System_msgAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)
    list_display = ('datadate','userid','msgtype','msgstatus','msgtitle','msg',)
    search_fields = ('userid','msgtype','msg',)
    fieldsets = (
        (None, {
            'fields': ('userid','target','msgstatus','msgtitle','msg',)
        }),
    )

@admin.register(Publish_apk)
class Publish_apkAdmin(admin.ModelAdmin):
    list_display = ('versioncode','versionName','apkname','apkinfo','datadate',)
    search_fields = ('versioncode','versionName','apkname','apkinfo',)
    fieldsets = (
        (None, {
            'fields': ('versioncode','versionName','apkname','apkinfo','apk')
        }),
    )

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "adtype":
            kwargs['choices'] = (
                ('fx','发现页广告'),
                ('dz','私人订制页广告'),
                ('atc1','文章列表页广告(大)'),
                ('atc2','文章列表页广告(小)'),
                ('yz','验证页广告'),
                ('hy','进入APP欢迎页'),
            )
        return super(AdvertisementAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)
    list_display = ('adtype','url','img',)
    search_fields = ('adtype','url',)
    fieldsets = (
        (None, {
            'fields': ('adtype','url','img')
        }),
    )
    
@admin.register(Listingimg)
class ListingimgAdmin(admin.ModelAdmin):
    list_display = ('listingid','img','imgname','imgtype',)
    search_fields = ('listingid','imgtype',)
    fieldsets = (
        (None, {
            'fields': ('listingid','img','imgname','imgtype',)
        }),
    )