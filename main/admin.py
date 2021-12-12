from django.contrib import admin

from .models import Athlete, Race, Activity

admin.site.register(Athlete)
admin.site.register(Race)
admin.site.register(Activity)
