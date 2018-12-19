from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^all$', views.all_issues),
    url(r'^my$', views.my_issues),
    url(r'^priority$', views.priority_issues),
    url(r'^team$', views.team_issues),
    url(r'^create$', views.create_form),
    url(r'^(?P<slug>[a-zA-Z]+)-(?P<issueno>[0-9]+)$', views.issue),
]
