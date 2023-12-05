# Generated by Django 3.2.5 on 2023-12-05 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0008_auto_20231205_1856'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='contributors',
        ),
        migrations.AlterField(
            model_name='issue',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='support.project'),
        ),
    ]