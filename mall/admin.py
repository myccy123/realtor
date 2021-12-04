# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Product_info,Product_sets,Orders,Product_detail

# Register your models here.

@admin.register(Product_info)
class Product_infoAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name','product_title','product_desc',)
    search_fields = ('product_id', 'product_name','product_title','product_desc',)
    list_filter = ('product_id',)
    fieldsets = (
        (None, {
            'fields': ('product_id', 'product_name','product_title','product_desc','price','product_img',)
        }),
    )

@admin.register(Product_sets)
class Product_setsAdmin(admin.ModelAdmin):
    list_display = ('set_id', 'product_id','set_name','set_price',)
    search_fields = ('set_id', 'product_id','set_name','set_price',)
    list_filter = ('set_id', 'product_id',)
    fieldsets = (
        (None, {
            'fields': ('set_id', 'product_id','set_name','set_price',)
        }),
    )


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('createdate','set_id', 'product_id','set_price','userid','order_status',)
    search_fields = ('set_id', 'product_id','set_price','userid','order_status',)
    list_filter = ('set_id','product_id',)
    fieldsets = (
        (None, {
            'fields': ('createdate','set_id', 'product_id','set_price','userid','tel','addr','order_status',)
        }),
    )
    
@admin.register(Product_detail)
class Product_detailAdmin(admin.ModelAdmin):
    list_display = ('product_id','orderid', 'product_text','product_img',)
    search_fields = ('product_id','product_text',)
    list_filter = ('product_id',)
    fieldsets = (
        (None, {
            'fields': ('product_id','orderid','detail_type', 'product_text','product_img',)
        }),
    )
