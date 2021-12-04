from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^list/', news_list),
    url(r'^rcmd/news/', get_rcmd_news),
    url(r'^(?P<lid>[0-9]+)', news_page),
    url(r'^share/cnt/', get_share_cnt),
]
