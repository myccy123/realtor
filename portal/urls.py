from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^count/', get_count),
    url(r'^agents/', agent_list),
    url(r'^listings/', listing_list),
    url(r'^corps/', friend_corps),
    url(r'^articles/', article_list),
    url(r'^agent/(?P<uid>[0-9]+)', agent_detail),
    url(r'^agent/listings/', agent_listings),
    url(r'^chinese/service/', chinese_service),
    url(r'^listing/info/', listing_info),
    url(r'^commit/email/', commit_email),
    url(r'^get/crumbs/', get_crumbs),
    url(r'^get/nearby/', get_nearby),
    url(r'^get/agent/of/listing/', get_agent_of_listing),
    url(r'^get/rcmd/listings/', get_recommend_listings),
    url(r'^city/price/', city_avg_price),
    url(r'^new/listings/', new_listings),
    url(r'^smart/flyer/', smart_flyer),
]
