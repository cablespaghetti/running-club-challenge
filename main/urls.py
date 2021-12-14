from django.urls import path

from . import views

urlpatterns = [
    path('race/<int:race_id>/results/', views.race_results, name='race_results'),
    path('', views.index, name='index'),
]
