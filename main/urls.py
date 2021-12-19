from django.urls import path

from . import views

urlpatterns = [
    path('race/<int:race_id>/results/', views.race_results, name='race_results'),
    path('submit_result', views.submit_result, name='submit_result'),
    path('', views.index, name='index'),
]
