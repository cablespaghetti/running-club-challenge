# Generated by Django 4.0 on 2021-12-18 22:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_activity_evidence_file_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='evidence_image',
        ),
    ]
