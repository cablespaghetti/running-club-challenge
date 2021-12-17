import datetime
import logging

from allauth.socialaccount.models import SocialAccount, SocialToken
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from stravalib import unithelper
from stravalib.client import Client

from agegrader.agegrader import AgeGrader
from .models import Athlete, Race, Activity

logger = logging.getLogger()


def create_update_athlete(user, gender=None, dob=None, photo=None):
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

    if photo:
        athlete.photo = photo

    athlete.save()


# TODO: Stop assuming there's only one match
def create_update_activity(race, athlete, start_time, elapsed_time, strava_activity_id):
    age_grade = age_graded_percentage(
        age=get_athlete_age(athlete=athlete, date=start_time.date()),
        gender=athlete.gender,
        distance=race_distance_in_km(race),
        time=elapsed_time.total_seconds(),
    )
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


def get_athlete_age(athlete, date):
    date_of_birth = athlete.DOB
    if not date_of_birth:
        return None

    return date.year - date_of_birth.year - \
           ((date.month, date.day) < (date_of_birth.month, date_of_birth.day))


def get_user_strava_token(user):
    social_accounts = SocialAccount.objects.filter(user=user)
    if social_accounts:
        social_tokens = SocialToken.objects.filter(account=social_accounts[0])
        if social_tokens:
            return social_tokens[0]
    return False


def update_user_strava_token(token):
    if token.expires_at < datetime.datetime.now(tz=datetime.timezone.utc):
        client = Client()
        refresh_response = client.refresh_access_token(
            client_id=token.app.client_id,
            client_secret=token.app.secret,
            refresh_token=token.token_secret
        )
        token.token = refresh_response['access_token']
        token.secret = refresh_response['refresh_token']
        token.expires_at = datetime.datetime.utcfromtimestamp(refresh_response['expires_at'])
        token.save()
        logger.info(f"Refreshed Strava token for {token.account}")
    logger.info(f"Did not need to refresh Strava token for {token.account}")


# TODO: Error handling
def get_athlete_for_user(user):
    return Athlete.objects.get(user=user)


def update_user_strava_activities(user):
    token = get_user_strava_token(user)
    if not token:
        logger.warning(f"Could not refresh {user}'s strava activities. No token.")
        return
    logger.debug(f"Got strava token for {user}")
    update_user_strava_token(token)
    a_week_ago = datetime.datetime.now() - datetime.timedelta(days=365)  # Todo reduce
    client = Client()
    client.access_token = token.token
    client.refresh_token = token.token_secret
    client.token_expires_at = token.expires_at
    strava_activities = client.get_activities(after=a_week_ago)
    races = Race.objects.all()
    for strava_activity in strava_activities:
        if strava_activity.type == 'Run' and strava_activity.workout_type == 1:
            for race in races:
                race_distance_km = race_distance_in_km(race)
                strava_distance_km = unithelper.kilometers(strava_activity.distance).num
                if race.start_date <= strava_activity.start_date.date() <= race.end_date \
                        and race.match_text.lower() in strava_activity.name.lower() \
                        and race_distance_km <= strava_distance_km \
                        < (race_distance_km + 0.1):
                    logger.info(
                        f"Found new match for race {race.name}: {strava_activity.name} for {user.first_name} {user.last_name} of distance {strava_distance_km}km at {strava_activity.start_date} and time {strava_activity.elapsed_time}")
                    create_update_activity(
                        race=race,
                        athlete=get_athlete_for_user(user),
                        start_time=strava_activity.start_date,
                        elapsed_time=strava_activity.elapsed_time,
                        strava_activity_id=strava_activity.id,
                    )


def race_distance_in_km(race):
    if race.distance_unit == "M":
        race_distance_km = race.distance * 1.609344
    else:
        race_distance_km = race.distance
    return race_distance_km


def age_graded_percentage(age, gender, distance, time):
    if not age:
        return 0
    age_grader = AgeGrader()
    age_graded_performance_factor = age_grader.age_graded_performance_factor(age, gender, distance, time)
    return age_graded_performance_factor * 100
