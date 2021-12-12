from django.db import models


class Athlete(models.Model):
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    # Based on Strava API definition not mine
    # https://developers.strava.com/docs/reference/#api-models-SummaryAthlete
    GENDER_CHOICES = [
        ('F', 'Female'),
        ('M', 'Male'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField()
    photo = models.CharField(max_length=254)
    strava_id = models.BigIntegerField()
    strava_access_token = models.CharField(max_length=1024)
    strava_refresh_token = models.CharField(max_length=1024)
    strava_expires_at = models.FloatField()
    strava_reauth_required = models.BooleanField(default=False)


class Race(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    distance = models.IntegerField()
    DISTANCE_UNIT_CHOICES = [
        ('M', 'Miles'),
        ('K', 'Kilometres'),
    ]
    distance_unit = models.CharField(max_length=1, choices=DISTANCE_UNIT_CHOICES)
    strava_segment_id = models.BigIntegerField()


class Activity(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    time = models.DateTimeField()
    evidence = models.CharField(max_length=1024)
    strava_activity_id = models.BigIntegerField()
