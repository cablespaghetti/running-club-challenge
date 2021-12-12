from django.db import models


class Athlete(models.Model):
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    # Based on Strava API definition not mine
    # https://developers.strava.com/docs/reference/#api-models-SummaryAthlete
    GENDER_CHOICES = [
        ('F', 'Female'),
        ('M', 'Male'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField(name="DOB", verbose_name="Date of Birth", blank=True, null=True)
    photo = models.CharField(max_length=254, verbose_name="Profile Photo URL", blank=True, null=True)
    strava_id = models.BigIntegerField(verbose_name="Strava ID", editable=False)
    strava_access_token = models.CharField(max_length=1024, editable=False)
    strava_refresh_token = models.CharField(max_length=1024, editable=False)
    strava_expires_at = models.FloatField(editable=False)
    strava_reauth_required = models.BooleanField(default=False, editable=False)


class Race(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=254)
    start_date = models.DateField()
    end_date = models.DateField()
    distance = models.IntegerField()
    DISTANCE_UNIT_CHOICES = [
        ('M', 'Miles'),
        ('K', 'Kilometres'),
    ]
    distance_unit = models.CharField(max_length=1, choices=DISTANCE_UNIT_CHOICES)
    strava_segment_id = models.BigIntegerField(blank=True, null=True)


class Activity(models.Model):
    def __str__(self):
        return f"{self.race.name} - {self.athlete.first_name} {self.athlete.last_name} - {self.time}"

    class Meta:
        verbose_name_plural = "activities"

    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    time = models.DateTimeField()
    evidence = models.CharField(max_length=1024, blank=True, null=True)
    strava_activity_id = models.BigIntegerField(blank=True, null=True)
