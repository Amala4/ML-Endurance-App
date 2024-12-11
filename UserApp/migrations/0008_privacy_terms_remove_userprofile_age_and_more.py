# Generated by Django 5.1.3 on 2024-11-29 18:40

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0007_alter_userprofile_metrics_unit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Privacy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Privacy Policy', max_length=300)),
                ('content', ckeditor.fields.RichTextField(blank=True, max_length=5000, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Privacy Policy',
            },
        ),
        migrations.CreateModel(
            name='Terms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Terms and Condition', max_length=300)),
                ('content', ckeditor.fields.RichTextField(blank=True, max_length=5000, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Terms and Condition',
            },
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='age',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, max_length=254, unique=True),
        ),
    ]
