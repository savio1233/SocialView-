# Generated by Django 4.2 on 2024-01-08 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hsApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='detection',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
