from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from main.models import Activity, Race


@login_required
def race_results(request, race_id):
    race = get_object_or_404(Race, id=race_id)

    activities = Activity.objects.filter(race=race).order_by('elapsed_time')
    results_dict = {'F': [], 'M': []}
    processed_athlete_list = []
    for activity in activities:
        if activity.athlete not in processed_athlete_list:
            results_dict[activity.athlete.gender].append(activity)
            processed_athlete_list.append(activity.athlete)
    template_context = {
        'race_name': race.name,
        'results_dict': results_dict,
    }
    return render(request, 'main/race_results.html', template_context)


@login_required
def index(request):
    races = Race.objects.all()
    template_context = {
        'race_list': races
    }
    return render(request, 'main/index.html', template_context)
