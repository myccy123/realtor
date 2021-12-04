from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^devauth/', dev_auth),
    url(r'^jsapi/', get_signature),
    url(r'^MP_verify_eVgil9IPg5X9lWOQ.txt$', get_secure_url),
]
