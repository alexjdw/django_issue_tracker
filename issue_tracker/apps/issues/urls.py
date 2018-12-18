from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^all$', views.all_issues),
    url(r'^my$', views.my_issues),
    url(r'^priority$', views.priority_issues),
    url(r'^(?P<issueno>[0-9]+)$', views.issue),
]
