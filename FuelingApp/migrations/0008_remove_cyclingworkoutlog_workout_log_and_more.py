# Generated by Django 5.1.3 on 2024-11-29 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FuelingApp', '0007_workoutlog_date_added'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cyclingworkoutlog',
            name='workout_log',
        ),
        migrations.AlterModelOptions(
            name='fuelingissue',
            options={'verbose_name_plural': 'Fueling Issue Logs'},
        ),
        migrations.AlterModelOptions(
            name='fuelingplan',
            options={'verbose_name_plural': 'Workout Fueling Plans'},
        ),
        migrations.AlterModelOptions(
            name='workoutcondition',
            options={'verbose_name_plural': 'Workout Condition Logs'},
        ),
        migrations.DeleteModel(
            name='CyclingWorkoutDetails',
        ),
        migrations.DeleteModel(
            name='CyclingWorkoutLog',
        ),
    ]
