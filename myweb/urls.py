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
from django.conf.urls import url, include
from django.contrib import admin
from singlepage.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.views import static as static_view
from web.views import index, console_page_redirect, signup_page_redirect, \
    login_page_redirect

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^app/', include('app.urls', namespace='app')),
    url(r'^weixin/', include('weixin.urls', namespace='weixin')),
    url(r'^news/', include('news.urls', namespace='news')),
    url(r'^web/', include('web.urls', namespace='web')),
    url(r'^bi/', include('bi.urls', namespace='bi')),
    url(r'^sp/', include('singlepage.urls', namespace='sp')),
    url(r'^mall/', include('mall.urls', namespace='mall')),
    url(r'^portal/', include('portal.urls', namespace='portal')),
    url(r'^login/', login_page_redirect),
    url(r'^register/', signup_page_redirect),
    url(r'^dashboard/', console_page_redirect),
    url(r'^$', index),
]

if True:
    urlpatterns.append(url(r'^static/(?P<path>.*)$', static_view.serve,
                           {'document_root': settings.STATICFILES_DIRS[0]},
                           name='static'), )
    urlpatterns.append(url(r'^data/(?P<path>.*)$', static_view.serve,
                           {'document_root': settings.MEDIA_ROOT},
                           name='media'), )
