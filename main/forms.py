from django.forms import ModelForm
from main.models import Activity


class SubmitActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = ['race', 'start_time', 'elapsed_time', 'evidence_file']
