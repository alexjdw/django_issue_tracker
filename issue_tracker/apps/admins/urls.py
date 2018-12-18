from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^template$', views.template),
    url(r'^$', views.admin_home),
]
