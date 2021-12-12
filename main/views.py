from datetime import date

from django.http import HttpResponse
from django.conf import settings
from django.template import loader

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


def race_results(request, race_id):
    race = Race.objects.get(id=race_id)
    activities = Activity.objects.filter(race=race).order_by('-elapsed_time')
    template = loader.get_template('main/race_results.html')
    template_context = {
        'results_list': activities
    }
    return HttpResponse(template.render(template_context, request))


def index(request):
    today = date.today()
    #races = Race.objects.filter(start_date__lte=today).filter(end_date__gte=today)
    races = Race.objects.all()

    template = loader.get_template('main/index.html')
    template_context = {
        'race_list': races
    }

    return HttpResponse(template.render(template_context, request))