# Generated by Django 5.1.3 on 2024-11-17 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0005_userprofile_birth_date_alter_userprofile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='metrics_unit',
            field=models.BooleanField(default=True, editable=False, verbose_name='Metric Unit?'),
        ),
    ]
