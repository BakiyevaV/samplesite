from django.urls import path

from bboard.views import index, by_rubric, BbCreateView, about_us,contacts

urlpatterns = [
    path('add/', BbCreateView.as_view(), name='add'),
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('', index, name='index'),
    path('about/', about_us, name='about'),
    path('contacts/', contacts, name='contacts'),
]
