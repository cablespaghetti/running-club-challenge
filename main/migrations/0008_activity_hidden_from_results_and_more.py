# Generated by Django 4.0 on 2021-12-19 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0007_remove_activity_evidence_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="activity",
            name="hidden_from_results",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="activity",
            name="age_grade",
            field=models.FloatField(editable=False),
        ),
    ]
