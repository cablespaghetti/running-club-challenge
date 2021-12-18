from django.urls import path

from . import views

urlpatterns = [
    path('race/<int:race_id>/results/', views.race_results, name='race_results'),
    path('submit_activity', views.submit_activity, name='submit_activity'),
    path('', views.index, name='index'),
]
