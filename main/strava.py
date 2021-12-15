from .models import Athlete
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import logging


def create_update_athlete(user, gender=None, dob=None, photo=None):
    try:
        athlete = Athlete.objects.get(user=user)
    except ObjectDoesNotExist:
        athlete = Athlete(user=user)
    except MultipleObjectsReturned:
        logger = logging.getLogger()
        logger.warning("User {user.pk} has multiple associated Athletes")

    athlete.user = user
    if gender:
        athlete.gender = gender

    if dob:
        athlete.DOB = dob

    if photo:
        athlete.photo = photo

    athlete.save()
