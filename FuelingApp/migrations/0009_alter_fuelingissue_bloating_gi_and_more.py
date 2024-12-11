# Generated by Django 5.1.3 on 2024-12-11 17:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FuelingApp', '0008_remove_cyclingworkoutlog_workout_log_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fuelingissue',
            name='bloating_gi',
            field=models.PositiveIntegerField(blank=True, choices=[(0, 'None'), (5, 'Some'), (10, 'Severe')], default=0, null=True, validators=[django.core.validators.MaxValueValidator(10)], verbose_name='Bloating (GI)'),
        ),
        migrations.AlterField(
            model_name='fuelingissue',
            name='bonking',
            field=models.PositiveIntegerField(blank=True, choices=[(0, 'None'), (5, 'Some'), (10, 'Severe')], default=0, null=True, validators=[django.core.validators.MaxValueValidator(10)], verbose_name='Bonking'),
        ),
        migrations.AlterField(
            model_name='fuelingissue',
            name='cramping',
            field=models.PositiveIntegerField(blank=True, choices=[(0, 'None'), (5, 'Some'), (10, 'Severe')], default=0, null=True, validators=[django.core.validators.MaxValueValidator(10)], verbose_name='Cramping'),
        ),
        migrations.AlterField(
            model_name='workoutcondition',
            name='weather_condition',
            field=models.CharField(blank=True, choices=[('cold', 'Cold'), ('cool', 'Cool'), ('neutral', 'Neutral'), ('hot', 'Hot'), ('very_hot', 'Very Hot')], max_length=255, null=True, verbose_name='Perceived Weather Condition'),
        ),
    ]
