# -*- coding:utf-8 -*-
from django import template

register = template.Library()


@register.filter(name='tiny_agent_img')
def tiny_agent_img(value):
    return value.replace('/userimgs/','/agentimgs_small/').replace('/agentimgs/','/agentimgs_small/').replace('/sp_users/','/agentimgs_small/')

@register.filter(name='tiny_listing_img')
def tiny_listing_img(value):
    return value.replace('/listings/','/listings_small/')


