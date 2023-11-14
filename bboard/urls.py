from .views import index, by_rubric, BbCreateView
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('add/', BbCreateView.as_view() ,name = 'add')
]
