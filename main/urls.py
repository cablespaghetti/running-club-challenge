from django.urls import path

from . import views

urlpatterns = [
    path('authorize', views.authorize, name='authorize'),
    path('authorized', views.authorized, name='authorized'),
    path('athlete_activities', views.athlete_activities, name='athlete_activities'),
]
