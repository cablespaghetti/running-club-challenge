from django.db import models

class Athlete(models.Model):
    strava_id = models.BigIntegerField()
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    sex = models.CharField(max_length=1)
    photo = models.CharField(max_length=254)

class StravaAuth(models.Model):
    athlete_id = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=1024)
    refresh_token = models.CharField(max_length=1024)
    expires_at = models.FloatField()
