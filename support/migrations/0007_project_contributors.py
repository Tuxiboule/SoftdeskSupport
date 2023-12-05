# Generated by Django 3.2.5 on 2023-12-05 17:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('support', '0006_alter_contributor_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='contributors',
            field=models.ManyToManyField(related_name='contributed_projects', through='support.Contributor', to=settings.AUTH_USER_MODEL),
        ),
    ]
