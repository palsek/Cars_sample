# users/urls.py

from django.conf.urls import include, url
from users.views import dashboard, register, show

#app_name = 'users'

urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^dashboard/", dashboard, name="dashboard"),
    url(r"^register/", register, name="register"),
    url(r"^show/", show, name="show"),
]