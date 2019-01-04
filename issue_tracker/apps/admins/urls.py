from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^add-users/(?P<issueno>[0-9]+)$', views.add_user_to_issue),
    url(r'^set-owner/(?P<issueno>[0-9]+)$', views.set_owner),
    url(r'^edit-priority/(?P<issueno>[0-9]+)$', views.edit_priority),
    url(r'^$', views.admin_home),
]
