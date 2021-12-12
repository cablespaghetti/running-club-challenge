from django.http import HttpResponse
from django.conf import settings
from stravalib.client import Client

from main.models import Athlete, Activity, Race


def authorize(request):
    client = Client()
    authorize_url = client.authorization_url(client_id=settings.STRAVA_CLIENT_ID, redirect_uri='http://localhost:8000/authorized')
    return HttpResponse(f"Please connect the app with Strava <a href=\"{authorize_url}\">here</a>")


def authorized(request):
    client = Client()
    code = request.GET.get('code')
    token_response = client.exchange_code_for_token(client_id=settings.STRAVA_CLIENT_ID, client_secret=settings.STRAVA_CLIENT_SECRET, code=code)
    access_token = token_response['access_token']
    refresh_token = token_response['refresh_token']
    expires_at = token_response['expires_at']

    client.access_token = access_token
    client.refresh_token = refresh_token
    client.token_expires_at = expires_at

    athlete_response = client.get_athlete()
    
    athlete = Athlete(
        strava_id=athlete_response.id,
        first_name=athlete_response.firstname,
        last_name=athlete_response.lastname,
        gender=athlete_response.sex,
        photo=athlete_response.profile,
        strava_access_token=access_token,
        strava_refresh_token=refresh_token,
        strava_expires_at=expires_at
    )
    athlete.save()

    return HttpResponse(
        f"For {athlete.first_name} {athlete.last_name} ({athlete.strava_id}), I now have an access token {access_token}"
    )


def athlete_activities(request):
    athlete_id = request.GET.get('id')
    athlete = Athlete.objects.get(id=athlete_id)
    client = Client()
    client.access_token = athlete.strava_access_token
    client.refresh_token = athlete.strava_refresh_token
    client.expires_at = athlete.strava_expires_at
    client.get_activities(limit=1)
    for activity in client.get_activities():
        strava_activity = activity
        break

    race = Race.objects.get(id=1)
    activity = Activity(
        race=race,
        athlete=athlete,
        time=strava_activity.start_date_local,
        strava_activity_id=strava_activity.id,
    )
    activity.save()

    return HttpResponse("Stuff")

#todo refreshing when expired
