from django.conf.urls import url # URL
from .views import *

# Karışıklığı önlemek için
app_name = 'post'

urlpatterns = [

    url(r'^index/$', post_index, name="index"),

    url(r'^create/$', post_create, name='create'),

    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'), # ?P argüman tanımlamak için klasik ifade. d=digit; w herhangi bir karakter

    url(r'^(?P<slug>[\w-]+)/update/$', post_update, name="update"),

    url(r'^(?P<slug>[\w-]+)/delete/$', post_delete, name='delete'),

]
