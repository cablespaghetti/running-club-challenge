from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from main.calculators import get_activity_age_grade
from main.models import Athlete, Activity
import logging
import requests

logger = logging.getLogger()


def create_update_athlete(user, gender=None, dob=None, photo_url=None):
    try:
        athlete = Athlete.objects.get(user=user)
    except ObjectDoesNotExist:
        athlete = Athlete(user=user)
    except MultipleObjectsReturned:
        logger.warning("User {user.pk} has multiple associated Athletes")

    athlete.user = user
    if gender:
        athlete.gender = gender

    if dob:
        athlete.DOB = dob

    if photo_url:
        copy_athlete_photo(athlete, photo_url)

    athlete.save()


def copy_athlete_photo(athlete, photo_url):
    photo_response = requests.get(photo_url, allow_redirects=True)
    photo_extension = photo_url.split('.')[-1]
    return athlete.photo.save(f'{athlete.pk}.{photo_extension}', ContentFile(photo_response.content))


def create_update_activity(race, athlete, start_time, elapsed_time, strava_activity_id):
    age_grade = get_activity_age_grade(athlete, elapsed_time, race, start_time)
    existing_activities = Activity.objects.filter(race=race, athlete=athlete, strava_activity_id=strava_activity_id)
    for existing_activity in existing_activities:
        if existing_activity.start_time != start_time or existing_activity.elapsed_time != elapsed_time:
            existing_activity.start_time = start_time
            existing_activity.elapsed_time = elapsed_time
            existing_activity.age_grade = age_grade
            existing_activity.save()
            logger.info(f"Updating {existing_activity.id} with new times")
        else:
            logger.info(f"Matching activity {existing_activity.id} doesn't need updating")
        return

    # If no existing activities are returned then this will run
    logger.info(f"Creating new activity")
    activity = Activity(
        race=race,
        athlete=athlete,
        start_time=start_time,
        elapsed_time=elapsed_time,
        age_grade=age_grade,
        strava_activity_id=strava_activity_id,
    )
    activity.save()


def get_athlete_for_user(user):
    return Athlete.objects.get(user=user)
