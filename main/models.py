from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class Athlete(models.Model):
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Based on Strava API definition not mine
    # https://developers.strava.com/docs/reference/#api-models-SummaryAthlete
    GENDER_CHOICES = [
        ("F", "Female"),
        ("M", "Male"),
    ]
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, blank=True, null=True
    )
    dob = models.DateField(
        name="DOB", verbose_name="Date of Birth", blank=True, null=True
    )
    photo = models.URLField(
        max_length=254, verbose_name="Profile Photo URL", blank=True, null=True
    )

    @admin.display(boolean=True, description="Photo")
    def has_photo(self):
        if self.photo:
            return True
        return False


class Race(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=254)
    start_date = models.DateField()
    end_date = models.DateField()
    distance = models.IntegerField()
    DISTANCE_UNIT_CHOICES = [
        ("M", "Miles"),
        ("K", "Kilometres"),
    ]
    distance_unit = models.CharField(max_length=1, choices=DISTANCE_UNIT_CHOICES)
    strava_segment_id = models.BigIntegerField(blank=True, null=True)


class Activity(models.Model):
    def __str__(self):
        return f"{self.race.name} - {self.athlete.user.first_name} {self.athlete.user.last_name} - {self.elapsed_time}"

    class Meta:
        verbose_name_plural = "activities"

    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    elapsed_time = models.DurationField()
    evidence = models.URLField(max_length=1024, blank=True, null=True)
    strava_activity_id = models.BigIntegerField(blank=True, null=True)
