"""myweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from singlepage.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^listing/(?P<mls>\w+)/', index),
    url(r'^make/preimg/', make_preimg),
    url(r'^make/(?P<token>\w+)/', make_sp),
    url(r'^spread/(?P<mls>\w+)/', make_spread),
    url(r'^get/openhouse/', get_openhouse),
    url(r'^get/imgs/', get_listing_imgs),
    url(r'^get/floorplan/', get_floor_plan),
    url(r'^call/agent/', call_agent),
    url(r'^get/start/', get_start),
    url(r'^signup/', sign_up),
    url(r'^postcard/', post_credit_card),
    url(r'^bi/', single_page_bi),
    url(r'^small/listing/', make_small_listing_imgs),
    url(r'^smart/flyer1/(?P<mls>\w+)/', page_smart_flyer),
]
