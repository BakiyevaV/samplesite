from django.urls import path

from .views import UserCreateView,login_view,index

app_name = 'test'
urlpatterns = [
    path('reg/', UserCreateView.as_view(), name='registration'),
    path('login/', login_view, name='login'),
    path('test/', index, name='test')
]


