from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^template$', views.template),  # Route for testing the template
    url(r'^add-users/(?P<issueno>[0-9]+)$', views.add_user_to_issue),
    url(r'^set-owner/(?P<issueno>[0-9]+)$', views.set_issue_owner),
    url(r'^edit/(?P<issueno>[0-9]+)$', views.edit),
    url(r'^$', views.admin_home),
]
