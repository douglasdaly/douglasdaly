# Generated by Django 2.1.2 on 2019-01-03 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('douglasdaly', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteadminsettings',
            name='err_404_sentry',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='siteadminsettings',
            name='err_500_sentry',
            field=models.BooleanField(default=False),
        ),
    ]
