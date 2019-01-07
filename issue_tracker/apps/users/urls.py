from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^u/login$', views.login_page),
    url(r'^u/login_submit$', views.login_submit),
    url(r'^u/register_submit$', views.register_submit),
    url(r'^u/logout$', views.logout_route),
    url(r'^$', views.login_page),  # catchall for / and /u/
    url(r'^u/$', views.login_page)
]
