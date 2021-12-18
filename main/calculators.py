from agegrader.agegrader import AgeGrader


def get_activity_age_grade(athlete, elapsed_time, race, start_time):
    age_grade = age_graded_percentage(
        age=get_athlete_age(athlete=athlete, date=start_time.date()),
        gender=athlete.gender,
        distance=race_distance_in_km(race),
        time=elapsed_time.total_seconds(),
    )
    return age_grade


def get_athlete_age(athlete, date):
    date_of_birth = athlete.DOB
    if not date_of_birth:
        return None

    return date.year - date_of_birth.year - \
           ((date.month, date.day) < (date_of_birth.month, date_of_birth.day))


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
