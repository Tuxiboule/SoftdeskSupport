# Generated by Django 3.2.5 on 2023-12-05 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0004_alter_contributor_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contributor',
            name='joined_at',
        ),
        migrations.AlterField(
            model_name='contributor',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributors', to='support.project'),
        ),
    ]