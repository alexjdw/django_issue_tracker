from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^all$', views.all_issues),
    url(r'^my$', views.my_issues),
    url(r'^priority$', views.priority_issues),
    url(r'^team$', views.team_issues),
    url(r'^new$', views.create_form),
    url(r'^create$', views.create_form_submit),
    url(r'^(?P<category>[a-zA-Z]+)-(?P<issueno>[0-9]+)/log$', views.add_to_log),
    url(r'^category/$', views.all_categories),
    url(r'^category/(?P<category>[a-zA-Z]+)$', views.one_category),
    url(r'^(?P<issueno>[0-9]+)/log$', views.add_to_log),
    url(r'^(?P<issueno>[0-9]+)/own$', views.own_issue),
    url(r'^(?P<issueno>[0-9]+)/join$', views.join_issue),
    url(r'^mark-complete/(?P<issueno>[0-9]+)$', views.mark_complete),
    url(r'^drop/(?P<issueno>[0-9]+)$', views.drop_issue),
    url(r'^(?P<category>[a-zA-Z]+)-(?P<issueno>[0-9]+)$', views.issue),
    url(r'^(?P<issueno>[0-9]+)$', views.issue),
    url(r'^search$', views.search)
]
