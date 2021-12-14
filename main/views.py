import logging
from datetime import date

from django.http import HttpResponse, Http404
from django.conf import settings
from django.shortcuts import render, get_object_or_404

from stravalib.client import Client
from django.contrib.auth.decorators import login_required
from main.models import Athlete, Activity, Race


@login_required
def race_results(request, race_id):
    race = get_object_or_404(Race, id=race_id)

    activities = Activity.objects.filter(race=race).order_by('-elapsed_time')
    template_context = {
        'results_list': activities
    }
    return render(request, 'main/race_results.html', template_context)


@login_required
def index(request):
    today = date.today()
    #races = Race.objects.filter(start_date__lte=today).filter(end_date__gte=today)
    races = Race.objects.all()
    template_context = {
        'race_list': races
    }
    return render(request, 'main/index.html', template_context)
