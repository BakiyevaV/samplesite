from django.urls import path, re_path

from .views import UserCreateView,login_view

urlpatterns = [
    re_path(r'^r\w{2}/$', UserCreateView.as_view(), name='registration'),
    re_path(r'^l\w*/$', login_view, name='login'),
]


