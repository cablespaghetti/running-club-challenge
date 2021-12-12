from django.http import HttpResponse
from stravalib.client import Client

from main.models import Athlete


def authorize(request):
    client = Client()
    authorize_url = client.authorization_url(client_id=49170, redirect_uri='http://localhost:8000/collector/authorized')
    return HttpResponse(f"Please connect the app with Strava <a href=\"{authorize_url}\">here</a>")

def authorized(request):
    client = Client()
    code = request.GET.get('code')
    token_response = client.exchange_code_for_token(client_id=49170, client_secret='nope', code=code)
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
    strava_auth = Athlete.objects.get(athlete_id=athlete_id)
    client = Client()
    client.access_token = strava_auth.access_token
    client.refresh_token = strava_auth.refresh_token
    client.expires_at = strava_auth.expires_at
    for activity in client.get_activities():
        print(activity)
    return HttpResponse("Stuff")

#todo refreshing when expired
